# Coolify build and deployment decision guide

Use this reference when selecting a migration target. Coolify's interface and supported paths can change, so verify the linked documentation again before implementation.

## The three paths are different

| Path | Who builds the image? | What Coolify does | External build server? |
| --- | --- | --- | --- |
| Git/Dockerfile application with Coolify Build Server enabled | Coolify on the configured build server | Pushes the result to a registry, then the deployment server pulls and runs it | Yes, if the resource type currently supports the setting |
| Docker Image application | CI or another external publisher | Pulls a selected tag or digest on the deployment server and starts the container; it does not clone source or build | No Coolify build step occurs |
| Docker Compose deployment with `image:` values | CI or an external publisher | Deploys the Compose service graph using prebuilt images | The Compose deployment itself doesn't build those images |

Current official documentation says **Use a Build Server** is not available for Docker Compose applications. It requires a registry image name; Coolify pushes from the builder and the deployment server pulls. Confirm this in the current UI/docs rather than relying on community discussions. If Coolify's Docker Image resource is chosen instead, use CI to build and publish: that resource pulls images but does not use Coolify's build server.

A multi-service stack can remain Compose-based while switching selected services from `build:` to published `image:` references. Keep Compose when the deployment depends on its networks, volumes, health checks, dependency ordering, or multiple services. If the real goal is a single Docker Image resource, first prove that all required services can be externalized or otherwise managed safely.

## Build-server prerequisites and operations

The current Coolify guide calls for a container registry, source access, and matching CPU architecture between the builder and deployment target. The build-server host needs Docker and push credentials. The deployment host also needs pull credentials for private images. A server assigned a Builds only role cannot host the application; choose its role with care and verify whether fallback builds are enabled.

For Docker Image deployments, configure the repository plus a version tag or digest. A mutable tag such as `latest` can resolve to different content on later deployments. Prefer commit-specific or release tags; use a digest when the deployed bytes must be immutable. Set the internal listening port and all runtime configuration in Coolify.

For CI publishing, run checks before build/push and run the Coolify deploy webhook only after the intended image has been published. Keep registry and webhook credentials in the CI secret store. Authenticate every server that needs to push or pull.

## Official references

- [Build servers](https://coolify.io/docs/core/infrastructure/servers/build-servers): server roles, prerequisites, registry requirements, build-server selection, and Compose limitation.
- [Build and deployment model](https://coolify.io/docs/core/build-deployment-model): source builds, registry images, runtime configuration, and deployment lifecycle.
- [Docker Compose](https://coolify.io/docs/applications/builds/docker-compose): Compose resource behavior, service configuration, health checks, and networking.
- [Deploy a Docker image](https://coolify.io/docs/applications/deployments/docker-image): registry pull behavior, tags/digests, runtime settings, and what this resource skips.
- [Docker registries](https://coolify.io/docs/applications/builds/docker-registries): image push/pull and private registry authentication on relevant servers.
- [GitHub Actions](https://coolify.io/docs/applications/sources/github/actions): test, build, publish, and optional post-publish deployment trigger sequence.
