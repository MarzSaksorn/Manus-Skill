---
name: coolify-compose-image-migration
description: Plan and implement migrations from Docker Compose-based builds to registry-backed Docker Image or Dockerfile deployments on Coolify, especially when a Compose resource cannot use a dedicated external build server. Use when restructuring image builds, preserving local Compose, publishing to GHCR or another registry, or configuring separate build and deployment servers.
---

# Coolify Compose-to-Image Migration

Help teams move a Compose-based application build to a Coolify-compatible image pipeline without losing runtime behavior, local development, or deployment safety.

## Start with the deployment model

Read the repository's Dockerfile, Compose files, `.dockerignore`, CI workflows, environment templates, health checks, and deployment notes before editing. Identify every service, port, volume, network, secret, required runtime asset, and migration task. Determine which server builds the image and which server runs it.

Ask only for decisions that materially change the migration, such as whether production should remain multi-service, which registry and architecture to target, or whether the pipeline should trigger deployments automatically. Otherwise, preserve current behavior and state assumptions.

Use the current Coolify documentation, not remembered UI labels or old issue threads. Read the relevant build-server, Compose, Docker Image, registry, and CI docs. The bundled [decision guide](references/deployment-model.md) captures the important distinctions and official references.

Choose the path that matches the desired topology:

- **Single application image, Coolify performs the build:** use a standard Git/Dockerfile application and configure Coolify's build server when supported by the current release. Register the image name and registry credentials so the deployment server can pull the built image.
- **CI builds and publishes the image:** use GitHub Actions or the user's CI to test, build, and publish. Deploy with a Docker Image resource for one image, or retain a Compose resource that references published `image:` values for a multi-service deployment. This is an external CI build, not a Coolify build-server build.
- **Compose `build:` services need a dedicated Coolify build server:** verify current Coolify support before editing. If the Compose resource has no build-server option, do not try to force it through hidden or undocumented settings. Either convert the resource to a supported single-image Dockerfile application, or move image builds to external CI and change only the deployment definitions that must use `image:`.

Do not convert a multi-service production stack into one image just to move builds. Keep Compose when services depend on Compose-managed networking, volumes, startup ordering, or separate lifecycles. A single Docker Image resource cannot replace those contracts by itself.

## Migration workflow

1. **Map current behavior.** Record the Compose services and their build contexts, Dockerfiles, commands, ports, environment variables, networks, volumes, health checks, and dependencies. Identify services that contain persistent or clinical data. Treat secrets as runtime-only; never copy `.env` values into build arguments, labels, workflow logs, or image layers.

2. **Choose build and run boundaries.** For a Coolify build server, verify its server role, registry availability, architecture compatibility, and current supported resource types. For CI-built images, decide which service images CI must publish and whether Coolify should use a Docker Image resource or continue to deploy Compose with `image:` references. Keep the production runtime contract explicit.

3. **Preserve local development.** Keep `docker-compose.yml` as the local development path unless the user explicitly asks to change it. If the repository needs a registry-only deployment definition, add a clearly named separate file or use the appropriate Coolify resource; do not silently replace the local Compose workflow. Do not remove a Compose file merely because Coolify will no longer build from it.

4. **Make the image production-ready.** Confirm the Dockerfile's build context, multi-stage build, lockfile-based dependency install, runtime assets, non-root user, port, health check, and graceful process startup. Ensure `.dockerignore` excludes `.env`, certificates, credentials, local dependencies, test output, and irrelevant data while retaining everything the runtime needs. Never bake mounted runtime secrets or certificate files into the image.

5. **Create a reproducible image pipeline.** Run checks before publishing. Build from the correct Dockerfile and context, target the deployment architecture, authenticate with least-privilege registry credentials, and publish a commit-specific immutable tag. Add a mutable convenience tag only if the deployment process intentionally uses it. Make Coolify's deploy webhook/API call the final step, after tests and successful image publication, and keep its token in CI secrets. Never claim a Coolify deployment uses its build server when CI built the image.

6. **Configure Coolify.** For a Coolify-built Dockerfile app, set the registry image name, enable the supported build-server setting, and authenticate both the build server (push) and deployment server (pull). For a Docker Image app, set the image reference and internal port, runtime environment, storage mounts, domain, and health check; authenticate the deployment server for private images. For Compose with prebuilt images, configure all service image tags and preserve networks, volumes, health checks, and service relationships.

7. **Validate without risking production.** Run repository tests, type checks, production builds, Dockerfile builds, and `docker compose config` where applicable. Verify the image exists under the expected registry and tag, test registry pulls from the servers that need them, and review runtime configuration and mount readability. Use an approved staging target for smoke tests. Never deploy, change production secrets, migrate data, delete volumes, or alter live Coolify configuration without explicit user approval.

8. **Document and hand off.** Explain which system builds, which server pulls and runs, which image reference is deployed, and how updates are triggered. Document required registry credentials, runtime environment variables, mounts, ports, health checks, and rollback to a known-good image tag or digest. State clearly whether local Compose remains supported and list anything not tested.

## Guardrails

- Do not invent Coolify capabilities or infer them from old issues. Re-check current official docs before each migration.
- Do not equate a Docker Image deployment with an external Coolify build-server deployment. A Docker Image resource pulls a published image and skips the source build; Coolify's build-server feature builds source-based application images and pushes them to a registry.
- Keep source builds separate from runtime secrets and persistent data.
- Preserve production services, volumes, networks, health behavior, ports, and startup dependencies unless the user approves a specific change.
- Treat pushing to a registry, triggering a deployment, merging, and production configuration changes as distinct actions. Obtain authorization for each action the user has not requested.
- Report any limitations in build or runtime validation. A successful image build does not prove that Coolify can pull it, start it, or serve the application.
