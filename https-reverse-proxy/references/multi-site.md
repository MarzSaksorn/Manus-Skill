# Multi-Site Caddy Routing

Use one Caddy process/container to own public TCP ports 80 and 443. Each hostname becomes a separate site block, and each block routes to an app's internal address:

```caddyfile
{
	admin off
}

care.example.com {
	reverse_proxy woundcare:3000
}

reports.example.com {
	reverse_proxy reports:8080
}
```

Point both hostnames to the same public IP. Caddy selects the site from the HTTP `Host` / TLS SNI name, obtains certificates for the configured names, and redirects HTTP to HTTPS. Keep all application services on a Docker network reachable by Caddy. Don't publish those app ports on the host unless a separately reviewed access path requires it.

## Separate Compose projects

A Compose service name resolves only on a shared Docker network. If the proxy and applications live in different Compose projects, create or reuse a named external network and attach each proxy/app service to it:

```yaml
networks:
  edge:
    external: true
    name: edge
```

Create that network once with `docker network create edge` only after confirming the target host and existing network state. Each relevant service must declare `networks: [edge]`. Keep existing public listeners and app networks intact; do not migrate them implicitly.

## Port ownership and deployment checks

Before adding a second site, inspect the running proxy and configuration to confirm which container owns ports 80/443. Make only the new hostname route change and validate it before reload. Preserve current site blocks and certificate volumes. For staging, confirm both domains resolve to the expected host, the HTTP requests redirect, and each HTTPS certificate and upstream route match the intended hostname. DNS, firewall, and live proxy changes require deployment approval.
