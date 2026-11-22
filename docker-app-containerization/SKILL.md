---
name: docker-app-containerization
description: Containerize web apps and services with maintainable Dockerfiles and Docker Compose. Use when adding or improving Docker builds, runtime images, app service definitions, environment handling, persistence, health checks, or container validation. Does not configure reverse proxies or TLS termination.
---

# Docker App Containerization

## Purpose and scope

Package an existing website, API, worker, or full-stack app as reproducible Docker images and Compose services. Preserve the app's current contracts and deployment boundary. This skill covers the application containers only; it does not configure Caddy, Nginx, Traefik, Cloudflare Tunnel, public TLS, or HTTP-to-HTTPS redirects. Use a reverse-proxy skill when the request includes those tasks.

## Workflow

### 1. Inspect the project before editing

Identify the language/runtime, package manager and lockfile, build/start scripts, output directory, listening port, expected health endpoint, and required runtime assets. Read existing Docker, Compose, ignore, environment, and deployment files first. Check whether the app binds to `0.0.0.0` inside a container; binding only to container loopback prevents access from other containers or the host.

Separate build-time values from runtime configuration. Identify secrets, external services, persistent data, migrations, model files, native modules, and OS packages. Do not assume that a database should be containerized just because the app is.

### 2. Build a reproducible image

Prefer a multi-stage build when the build toolchain or development dependencies aren't needed at runtime. Pin a supported base image tag and install dependencies from the project's lockfile using its frozen/clean-install mode. Copy only the files required by each stage, and preserve required assets such as migrations, ONNX models, templates, certificates, or static files explicitly.

Run the app as a non-root user when the image supports it. Use an init process where appropriate so the app receives termination signals and reaps child processes. Keep `CMD` exec-form so signals reach the process. Exclude `.env`, credentials, `.git`, local dependencies, caches, test artifacts, and unrelated training or data files with `.dockerignore`; don't exclude assets the runtime actually needs.

Don't blindly reuse a generic Dockerfile. Adapt it to the framework's production server, output layout, package-manager workspace, native dependencies, and runtime requirements. A static frontend may need a static server image; an SSR app needs its Node or other server runtime.

### 3. Define Compose services

Create or update Compose services to reflect the actual app topology. Keep configuration in runtime environment variables or mounted secret files, not in image layers or source control. Commit an `.env.example` with names and safe placeholders, and make the real `.env` ignored.

Publish a host port only when the user wants direct access to the app. The bundled Compose template binds to host loopback by default, which supports local access without exposing the service to the LAN. For container-to-container traffic, use a Compose network and service DNS; use `expose` only as documentation or when the port needs to be declared. Do not attach a reverse proxy as part of this skill.

Use named volumes only for data that must survive container recreation. Avoid mounting source code or node_modules into production containers. Add restart behavior and health checks only when the application has a real, reliable health endpoint or test. Use `depends_on` health conditions only for startup ordering; application code must still handle dependency outages and reconnections.

### 4. Validate the result

Run `docker compose config` to catch Compose syntax and interpolation errors. Build with `docker compose build` or `docker build`; inspect failures fully before changing dependencies or disabling checks. Start the service only in the approved local or staging environment, then verify container health and the app's documented endpoint. Run repository type checks, tests, and production build when source or build steps changed.

If Docker isn't installed or the target runtime isn't available, report that limitation and perform only checks supported by the environment. Don't claim that an image starts or works without a runtime smoke test.

### 5. Protect production boundaries

Treat Docker builds and Compose edits as repository changes, not permission to deploy. Before starting, replacing, or exposing a production service, obtain explicit approval and confirm the target host, data volumes, port bindings, environment secrets, and rollback path. Never delete a volume, migrate production data, alter firewall rules, or publish a service publicly without explicit authorization.

## Common failure checks

- **Build context too large or secret found in image:** review `.dockerignore`, build context, image layers, and build arguments. Rotate a secret if it entered an image or repository; removing the latest layer doesn't erase earlier layers.
- **Container starts but host can't reach it:** check host port mapping, app bind address, listening port, container health, and host firewall. Keep host exposure consistent with the requested access boundary.
- **Container can't resolve another service:** use its Compose service name on a shared network, not `localhost`; inside a container, `localhost` refers to that same container.
- **Restart loop:** read the full container logs and exit code. Check required runtime assets, environment variables, file permissions, startup migrations, and native library compatibility.
- **Data disappears after recreation:** persist only the correct application data directory in a named volume and verify backup/restore before production changes.
- **Native module or ONNX/ML runtime fails:** build and run on compatible OS/libc/CPU architecture, include required native packages and model files, and test on the deployment architecture.

## Bundled templates

Use `templates/Dockerfile.node-npm.template` as a starting point for a conventional Node server built with npm. Adapt the output and entry point. Use `templates/compose.node-web.yml.template` for a direct local app service with loopback-only host publishing. Use `templates/.dockerignore.node.template` for a typical Node repository and add project-specific exclusions carefully.
