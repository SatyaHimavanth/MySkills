# Networking — Production

## Purpose

Define the trusted proxy and routing boundary for production FastAPI deployments.

## Rules

- Configure the exact trusted proxy/load-balancer addresses or trusted-hop model supported by the deployment.
- Validate HTTPS/host/forwarded-header behavior through deployment tests.
- Align body-size and timeout policies across WAF, proxy, load balancer, and FastAPI.
- Preserve request/trace IDs across the routing chain.
- Use readiness to decide whether an instance receives traffic.

## Forbidden

- trusting arbitrary `X-Forwarded-*` headers
- assuming the application sees the public client address without proxy configuration
