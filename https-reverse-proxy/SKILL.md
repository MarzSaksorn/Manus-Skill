---
name: https-reverse-proxy
description: Configure or troubleshoot HTTPS reverse proxies for self-hosted web apps, especially Caddy with Docker Compose. Use when adding automatic TLS, HTTP-to-HTTPS redirects, multiple domains on one host, resolving ports 80/443 conflicts, or keeping app containers private behind a shared proxy.
---

# HTTPS Reverse Proxy

## Overview

Set up a single reverse proxy as the public entry point for one or more web apps. Prefer Caddy for straightforward automatic certificates and HTTPS redirects; adapt to an existing Nginx, Traefik, or Caddy deployment rather than creating a competing listener.

## Workflow

### 1. Inspect the host and deployment

Before editing, inspect the repository and target host configuration:

- Find existing `Dockerfile`, Compose files, proxy configs, env templates, deployment docs, and health checks.
- Identify the app's internal listen port, container/service name, network, and whether it serves HTTP or HTTPS internally.
- Check whether a proxy already owns ports 80 and 443. Inspect `docker ps`, Compose projects, and `ss -ltnup` where authorized.
- Determine whether the endpoint is public or private (for example, Tailscale-only). Don't expose a private clinical or internal app to the public internet just to obtain TLS.
- Identify the actual hostname(s), DNS owner, firewall owner, and deployment target. Never invent a domain or assume DNS is configured.

If the user only wants a configuration change, prepare files and instructions without starting or deploying services. Ask for the hostname and target environment when those values are needed to make a live endpoint work.

### 2. Choose the proxy topology

- **Existing proxy on the same host:** Add a hostname route to that proxy. Do not launch another service that binds host ports 80/443.
- **No existing proxy:** A single Caddy container can publish host ports 80/443 and route to app containers on a shared Docker network.
- **Multiple apps:** Keep one proxy and map each distinct hostname to its app's internal service/port. Do not assign host ports 80/443 to each app.
- **Private tailnet-only app:** Preserve the access boundary. Use the approved tailnet HTTPS endpoint or a private TLS arrangement rather than opening public ingress.

Read `references/multi-site.md` when adding a site beside existing services or when Compose projects use separate networks.

### 3. Configure Caddy + Compose

Use `templates/Caddyfile.template` as a starting point. Adapt site name, app service, and internal port to the inspected project.

For an app in the same Compose project:

- Publish only Caddy's `80:80` and `443:443` (optionally `443:443/udp` for HTTP/3).
- Keep the application port private to the Compose network with `expose` or internal networking. Remove host `ports` mappings for the app when the intended access path is HTTPS-only.
- Reverse proxy to the Compose service DNS name, not `localhost` or the host-published port.
- Persist Caddy `/data` and `/config` with named volumes so ACME account and certificate state survive recreation.
- Gate proxy startup on app health when a reliable health check exists; otherwise handle startup/retry behavior explicitly.
- Require a non-empty site hostname through an environment variable and keep credentials out of committed files.
- Preserve app auth and authorization. TLS at the proxy does not secure an unauthenticated application.

Caddy automatically obtains certificates and redirects HTTP to HTTPS when configured with a real hostname. Don't add HSTS by default; it has sticky browser behavior and needs a deliberate domain/subdomain policy.

### 4. Document operational prerequisites

State clearly that certificate issuance and renewals require:

- The domain's DNS A/AAAA records to point to the host or its approved edge proxy.
- Inbound TCP port 80 and/or 443 reachable for the selected ACME challenge. Port 80 is needed for the common HTTP challenge; DNS challenges require separately configured DNS credentials and should not be improvised.
- Host and provider firewalls to permit intended traffic.
- No other process or container binding the same host ports.
- Persistent writable Caddy state.

Explain that an HTTP request should redirect to the HTTPS origin and that the certificate must validate for the exact hostname. Don't claim HTTPS is active until tested from outside the host.

### 5. Validate without deploying

Run the checks available in the current environment:

1. Format and inspect changed files; run `git diff --check`.
2. Validate Compose with `docker compose config` using the intended non-secret hostname/config. Avoid printing secrets from rendered configuration into logs.
3. Validate the Caddyfile with `caddy validate --config Caddyfile --adapter caddyfile` or the equivalent container command.
4. Run app tests/build if application files changed.
5. If a staging service is authorized, verify the HTTP redirect, TLS hostname/certificate, upstream response, and app/API behavior.

If Docker, Caddy, DNS, or a deploy target is unavailable, report that exact limit. Do not substitute static inspection for a live TLS verification.

### 6. Deploy only with explicit approval

A Git commit or push is not deployment approval. Before changing a live server, DNS record, firewall, production service, or clinical deployment, show the exact target, hostnames, ports, services, and impact, then get explicit confirmation. Preserve a rollback plan and existing proxy routes. Never overwrite or stop an existing listener just to resolve a conflict without authorization.

## Troubleshooting

- **Port bind error on 80/443:** Find the current listener and identify its owning service. Reuse the existing proxy or coordinate a planned migration; do not move the app to another external port as a workaround for standard HTTPS.
- **Certificate issuance fails:** Check exact DNS answers, public reachability, NAT/firewall rules, clock, ACME logs, challenge method, and persistent Caddy state. Ensure stale AAAA records don't point elsewhere.
- **502 Bad Gateway:** Check container health, shared network membership, service DNS name, internal port, and whether the app binds to `0.0.0.0` inside its container.
- **Redirect loop or insecure cookies:** Inspect upstream forwarded-protocol handling, auth callback/origin settings, and proxy trust behavior. Don't globally trust forwarded headers from arbitrary clients; only trust the known proxy path.
- **HTTPS works but app fails:** Check WebSocket/stream forwarding if used, request body limits, path handling, and app-generated absolute URLs.
- **Compose projects can't resolve each other:** Attach the proxy and apps to a shared external Docker network or route through the existing host-local proxy mechanism. Don't publish app ports publicly merely to cross project boundaries.

## Deliverable Checklist

- One clear proxy owner for host ports 80/443.
- Each hostname routes to the correct internal app service and port.
- App containers aren't independently exposed on public host ports when HTTPS-only access is required.
- Certificate and proxy state persist.
- DNS, firewall, hostname, and renewal prerequisites are documented.
- No production/DNS/firewall changes occurred without explicit confirmation.
- Verification distinguishes static config checks from live HTTPS checks.
