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

Avoid query-string bearer credentials where a safer authentication mechanism exists because URLs can leak through logs/intermediaries.

## Disconnect and cancellation

Treat disconnect as a normal state transition. Release DB sessions, Redis subscriptions, files, generators, and other request resources. If work must continue after disconnect, convert it to durable job execution instead of keeping request-bound work alive.

## Backpressure

Use bounded producer buffers. Do not accumulate unlimited stream data in memory.

## DB transactions

Do not keep transactions open for a long stream unless explicitly required. Prepare authoritative data, commit/close, then stream.

## Proxy/load balancer

Review idle/read/write timeouts, SSE buffering, WebSocket upgrade, max connection duration, and maximum concurrent long-lived connections. The smallest timeout in the chain can terminate the stream.

## Multi-replica events

Connections belong to one replica. If events must reach clients connected to different replicas, use shared pub/sub, Redis Streams, or a message broker. Do not rely on process-local subscriber maps.

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

