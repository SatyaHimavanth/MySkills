# Database Concurrency — Shared

## Purpose

Prevent lost updates, phantom writes, and race conditions across concurrent requests and background workers using database-level concurrency controls.

## Strategies

- **Atomic SQL updates**: Single-statement conditional state transitions.
- **Pessimistic locking**: SQL `SELECT ... FOR UPDATE` row locks.
- **Optimistic versioning**: Integer/timestamp version counters with conditional update checks.
- **Serializable isolation / DB constraints**: Database constraints to guarantee global invariants.

## Strategy 1: Atomic SQL Update

```python
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from myapp.models import Product

async def decrement_stock(session: AsyncSession, product_id: str, quantity: int) -> bool:
    stmt = (
        update(Product)
        .where(Product.id == product_id, Product.stock >= quantity)
        .values(stock=Product.stock - quantity)
    )
    result = await session.execute(stmt)
    return result.rowcount > 0  # Returns False if stock was insufficient
```

## Strategy 2: Pessimistic Row Locking (`FOR UPDATE`)

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from myapp.models import Account, AppError

async def transfer_funds(
    session: AsyncSession,
    from_id: str,
    to_id: str,
    amount: Decimal,
) -> None:
    # Acquire row locks in deterministic primary key order to prevent deadlocks
    first_id, second_id = sorted([from_id, to_id])

    stmt1 = select(Account).where(Account.id == first_id).with_for_update()
    stmt2 = select(Account).where(Account.id == second_id).with_for_update()

    res1 = await session.execute(stmt1)
    res2 = await session.execute(stmt2)

    from_account = res1.scalar_one() if first_id == from_id else res2.scalar_one()
    to_account = res2.scalar_one() if second_id == to_id else res1.scalar_one()

    if from_account.balance < amount:
        raise AppError(code="INSUFFICIENT_FUNDS", message="Balance too low", status_code=400)

    from_account.balance -= amount
    to_account.balance += amount
```

## Strategy 3: Optimistic Concurrency Control (`version_id_col`)

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.exc import StaleDataError

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(primary_key=True)
    status: Mapped[str]
    version: Mapped[int] = mapped_column(default=1, nullable=False)

    __mapper_args__ = {
        "version_id_col": version,
    }

async def update_order_status(session: AsyncSession, order_id: str, new_status: str):
    try:
        order = await session.get(Order, order_id)
        order.status = new_status
        await session.commit()
    except StaleDataError:
        await session.rollback()
        raise AppError(code="CONFLICT", message="Order was modified by another request", status_code=409)
```

## `NOWAIT` and `SKIP LOCKED`

PostgreSQL supports `NOWAIT` and `SKIP LOCKED` on row-locking clauses:
- `with_for_update(nowait=True)`: Fails immediately (`OperationalError`) instead of blocking when a lock is held.
- `with_for_update(skip_locked=True)`: Skips locked rows; appropriate for queue-like background worker consumption.

## Application Concurrency Checklist

For each write path ask:
1. Can two requests read the same old state?
2. Is the write conditional on observed state?
3. Is a DB constraint (`UNIQUE`, `CHECK`) protecting the invariant?
4. Should conflicting writes return HTTP `409 Conflict`?
5. Are row locks acquired in deterministic primary key order to prevent deadlocks?

## Forbidden

- Python process-level locks (`asyncio.Lock`) for multi-worker / multi-replica backend correctness
- read-then-write updates without row locking, atomic update, or version checking
- non-deterministic lock acquisition order across multiple rows
