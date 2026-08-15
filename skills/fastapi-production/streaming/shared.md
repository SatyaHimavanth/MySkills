# Streaming and WebSockets — Shared

## Purpose

Select and implement long-lived communication correctly for `StreamingResponse`, Server-Sent Events, and WebSockets. FastAPI documents async-generator cancellation concerns for streaming and dependency/security support for WebSocket endpoints.

## Protocol selection

### StreamingResponse
Use for files, generated data, NDJSON, and one-way progressive output.

### SSE
Use for one-way server-to-client events with browser-friendly reconnect behavior.

### WebSocket
Use for bidirectional low-latency communication.

Do not choose WebSockets by default when SSE is sufficient.

## StreamingResponse

```python
async def generate():
    for chunk in chunks:
        yield chunk
        await anyio.sleep(0)

return StreamingResponse(generate(), media_type='application/octet-stream')
```

FastAPI notes that an async generator needs an await point so cancellation can be observed, especially for long/infinite streams.

## Contracts

Streaming is not the normal JSON envelope. Document media type, chunk/event schema, terminal behavior, cancellation, and error behavior.

## SSE

Define `event`, `data`, `id`, `retry`, event schemas, heartbeats, reconnect rules, and terminal events.

## WebSocket auth

FastAPI supports dependencies/security in WebSocket endpoints. After connection establishment, use WebSocket close semantics rather than HTTP exceptions.

Avoid query-string bearer credentials where a safer authentication mechanism exists because URLs can leak through logs/intermediaries. For a bearer-JWT API (cookie-based session auth doesn't apply — there's no cookie), the concrete safer mechanism is **first-message auth**: accept the connection, then require the client's first WebSocket frame to carry the access token, with a timeout — not the URL. Verified end-to-end against a real backend:

```python
@router.websocket("/ws/tasks")
async def task_events(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        raw = await asyncio.wait_for(websocket.receive_text(), timeout=5)
        payload = decode_token(json.loads(raw)["token"], settings.auth.jwt_secret, settings.auth.algorithm)
        if payload.get("type") != "access":
            raise ValueError()
    except Exception:
        await websocket.close(code=4401, reason="unauthorized")
        return
```
Verified: an invalid/garbage token correctly closes with code 4401 and no data is exchanged first.

## Subscription readiness — verified race condition

If the endpoint subscribes to a pub/sub channel (or any other async setup) after auth, **send an explicit ack once that setup completes** — do not assume the client can safely trigger the first event right after sending its auth message. Verified directly: without an ack, a REST write issued immediately after the WS client sent its auth frame was silently dropped — the server's `pubsub.subscribe()` hadn't completed yet. Adding a client-side delay "fixed" it, which is the wrong fix (a timing guess, not a guarantee); the correct fix is a deterministic `{"type": "subscribed"}` message the client waits for before assuming it's safe to trigger anything event-producing.

## Disconnect and cancellation

Treat disconnect as a normal state transition. Release DB sessions, Redis subscriptions, files, generators, and other request resources. If work must continue after disconnect, convert it to durable job execution instead of keeping request-bound work alive.

**Verified bug: a bare `async for message in pubsub.listen(): await websocket.send_text(...)` loop does not reliably detect a client disconnect and leaks the Redis subscription.** `pubsub.listen()` only discovers the WebSocket is gone when it next tries to `send_text` on it — with no new pub/sub traffic, the loop blocks indefinitely and the subscription is never released. Confirmed directly: `PUBSUB NUMSUB` stayed at 1 indefinitely after a client-initiated disconnect with no further events. Fix: run a second task whose only job is `await websocket.receive_text()` in a loop (to detect the disconnect independently of Redis traffic), race it against the forwarding loop with `asyncio.wait(..., return_when=FIRST_COMPLETED)`, and unsubscribe/close in a `finally` after either one completes:

```python
async def forward_events():
    async for message in pubsub.listen():
        if message["type"] == "message":
            await websocket.send_text(message["data"])

async def watch_for_disconnect():
    while True:
        await websocket.receive_text()

forward_task = asyncio.create_task(forward_events())
watch_task = asyncio.create_task(watch_for_disconnect())
try:
    await asyncio.wait([forward_task, watch_task], return_when=asyncio.FIRST_COMPLETED)
finally:
    forward_task.cancel()
    watch_task.cancel()
    await pubsub.unsubscribe(channel)
    await pubsub.aclose()
```
Verified after this fix: subscriber count correctly returns to 0 immediately after disconnect.

## Backpressure

Use bounded producer buffers. Do not accumulate unlimited stream data in memory.

## DB transactions

Do not keep transactions open for a long stream unless explicitly required. Prepare authoritative data, commit/close, then stream.

## Proxy/load balancer

Review idle/read/write timeouts, SSE buffering, WebSocket upgrade, max connection duration, and maximum concurrent long-lived connections. The smallest timeout in the chain can terminate the stream.

## Multi-replica events

Connections belong to one replica. If events must reach clients connected to different replicas, use shared pub/sub, Redis Streams, or a message broker. Do not rely on process-local subscriber maps.

**Verified, not just asserted**: ran two genuinely separate `uvicorn` processes against the same PostgreSQL/Redis. Connected a WebSocket client to process B, issued the triggering write via REST to process A, confirmed the event still arrived on process B's connection via the shared Redis pub/sub channel. Cross-replica delivery via Redis pub/sub works as documented — the mechanism itself was never the issue in the bugs found while building this; both real bugs found (subscription-ready race, disconnect-leak) were protocol/lifecycle issues on top of a correctly-working delivery mechanism.

## Durable jobs vs streams

Use:

```text
POST /jobs → 202 + job_id → worker → shared progress → SSE/WebSocket/polling
```

Do not use a long-lived connection as the only record of job state.

## Forbidden

- infinite streams without cancellation
- unbounded buffers
- long DB transactions for streams
- process-local event state in multi-replica production
- query-string access tokens by default

## Sources

- https://fastapi.tiangolo.com/advanced/custom-response/
- https://fastapi.tiangolo.com/advanced/websockets/

