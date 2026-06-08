# Architecture

Use a 3-layer architecture for new code and for refactors:

- Presentation layer: HTTP adapters, Flask app factories, route/controller glue, request/response conversion.
- Application layer: use cases, orchestration, runtime decisions, transaction boundaries, service-level policies.
- Infrastructure layer: database models/sessions, logging, metrics, filesystem, subprocesses, network clients, external services.

## Current Layout

- `opennamu_forge/presentation/`: new presentation-layer code.
- `opennamu_forge/presentation/routes/`: Flask route modules. New or moved route modules must live here.
- `opennamu_forge/application/`: new application-layer code.
- `opennamu_forge/application/ports/`: protocol interfaces for infrastructure adapters.
- `opennamu_forge/application/dto/`: DTOs exchanged between application/presentation and infrastructure.
- `opennamu_forge/infrastructure/`: new infrastructure-layer code.
- Top-level `route/` must not exist. Do not add new modules there; route modules belong in `opennamu_forge/presentation/routes`.
- `opennamu_forge/presentation/routes/tool/`: legacy shared utility layer. New infrastructure code should go under `opennamu_forge/infrastructure/`; keep wrappers only for compatibility.

## Dependency Direction

- Presentation may depend on Application and Infrastructure only for adapter wiring.
- Application may depend on domain concepts and abstract protocols, but should not import Flask.
- Infrastructure may depend on external libraries and concrete implementations.
- Presentation routes must communicate with persistence through application ports/DTOs or explicit adapter factories.
- Wiki setting reads belong in `WikiSettingsService`; route modules should not query the `other` table directly.
- Infrastructure repository implementations must not leak SQLModel rows to presentation/application callers.
- Legacy route compatibility is exempt only until that area is actively refactored.

## Refactor Rule

When changing an existing feature:

1. Add characterization tests or integration tests for current expected behavior.
2. Move new behavior into the appropriate `opennamu_forge/*` layer.
3. Keep existing route signatures and URLs stable.
4. Leave compatibility wrappers when old imports are still used.
5. Remove wrappers only with a migration plan.
