# Architecture

Use a 3-layer architecture for new code and for refactors:

- Presentation layer: HTTP adapters, Flask app factories, route/controller glue, request/response conversion.
- Application layer: use cases, orchestration, runtime decisions, transaction boundaries, service-level policies.
- Infrastructure layer: database models/sessions, logging, metrics, filesystem, subprocesses, network clients, external services.

`opennamu_forge/config/` is a cross-cutting runtime config boundary, not a domain layer. It may parse `.env`, normalize runtime values, and expose typed config objects. It must not contain domain behavior, persistence adapters, Flask routes, SQLModel sessions, or external-process lifecycle code.
Runtime config builders must return typed config objects such as `DatabaseConfig` and `MonitoringConfig`. When legacy bootstrap code still needs the historical `db_set` dictionary shape, convert explicitly at the boundary with a named method such as `DatabaseConfig.to_db_set()`.

## Current Layout

- `opennamu_forge/presentation/`: new presentation-layer code.
- `opennamu_forge/presentation/routes/`: Flask route modules. New or moved route modules must live here.
- `opennamu_forge/presentation/route_registry.py`: central Flask URL rule registration for route modules and GopenNAMU delegated views.
- `opennamu_forge/presentation/runtime/`: runtime-only orchestration helpers for server startup options, GopenNAMU process lifecycle, and scheduled background jobs.
- `opennamu_forge/presentation/authorization_helpers.py`: ACL, ban, and level helpers backed by GopenNAMU APIs.
- `opennamu_forge/presentation/captcha_helpers.py`: captcha markup/session helpers. Captcha verification HTTP I/O belongs in infrastructure clients.
- `opennamu_forge/presentation/file_helpers.py`: image directory and default robots.txt helpers used by routes/runtime.
- `opennamu_forge/presentation/identity_helpers.py`: identity/IP display helpers backed by GopenNAMU APIs.
- `opennamu_forge/presentation/dependencies.py`: presentation dependency providers for repositories and application services.
- `opennamu_forge/presentation/rendering/`: document rendering adapters. Keep rendering code out of `presentation/shared`.
- `opennamu_forge/presentation/response_helpers.py`: template bridge, language lookup, redirects, domain loading, and simple response rendering helpers.
- `opennamu_forge/presentation/encoding_helpers.py`: URL encoding, hashing, and JSON encode/decode helpers used by routes/runtime/rendering.
- `opennamu_forge/presentation/email_helpers.py`: SMTP setting assembly for email routes. SMTP network I/O belongs in infrastructure clients.
- `opennamu_forge/presentation/text_helpers.py`: small text, numeric, cache suffix, and random-key helpers used by routes/runtime.
- `opennamu_forge/presentation/user_validation_helpers.py`: user-facing validation helpers used by registration and profile routes.
- `opennamu_forge/application/`: new application-layer code.
- `opennamu_forge/application/ports/`: protocol interfaces for infrastructure adapters.
- `opennamu_forge/application/dto/`: DTOs exchanged between application/presentation and infrastructure.
- `opennamu_forge/application/runtime_context.py`: process runtime values shared across startup and adapters.
- `opennamu_forge/config/`: runtime config builders for environment, database, monitoring, and future process options.
- `opennamu_forge/config/runtime_database.py`: runtime DB selection state used by repository factories. Presentation code must not own DB connection classes.
- `opennamu_forge/infrastructure/`: new infrastructure-layer code.
- Top-level `route/` must not exist. Do not add new modules there; route modules belong in `opennamu_forge/presentation/routes`.
- `opennamu_forge/presentation/shared/`: shared presentation helpers for route adapters. New infrastructure code should go under `opennamu_forge/infrastructure/`.
- `opennamu_forge/presentation/shared/func_render.py` and `func_render_namumark.py` must not exist; rendering code belongs in `opennamu_forge/presentation/rendering`.
- `opennamu_forge/presentation/routes/tool/` must not exist. Do not reintroduce a route-local tool package.
- Do not use wildcard imports in project code. Route modules and runtime wiring must import the exact helper names they use.

## Dependency Direction

- Presentation may depend on Application and Infrastructure only for adapter wiring.
- Presentation may depend on Config for runtime wiring values.
- Application may depend on domain concepts and abstract protocols, but should not import Flask.
- Infrastructure may depend on Config, external libraries, and concrete implementations.
- Presentation routes must communicate with persistence through application ports/DTOs or explicit adapter factories.
- Presentation route/runtime imports for repository and application-service providers must come from `opennamu_forge.presentation.dependencies`.
- Presentation route/runtime imports for ACL, ban, and level helpers must come from `opennamu_forge.presentation.authorization_helpers`.
- Presentation route imports for captcha helpers must come from `opennamu_forge.presentation.captcha_helpers`; external captcha verification I/O belongs in infrastructure.
- Presentation route/runtime imports for response helpers must come from `opennamu_forge.presentation.response_helpers`.
- Presentation route/runtime imports for URL/hash/JSON helpers must come from `opennamu_forge.presentation.encoding_helpers`.
- Presentation route imports for SMTP/email helpers must come from `opennamu_forge.presentation.email_helpers`; external SMTP I/O belongs in infrastructure.
- Presentation route/runtime imports for file helpers must come from `opennamu_forge.presentation.file_helpers`.
- Presentation route imports for identity/IP display helpers must come from `opennamu_forge.presentation.identity_helpers`.
- Presentation route/runtime imports for text helpers must come from `opennamu_forge.presentation.text_helpers`.
- Presentation route imports for user validation helpers must come from `opennamu_forge.presentation.user_validation_helpers`.
- Presentation routes must not depend on `from ... import *`; explicit imports are required so route dependencies remain auditable during migration.
- Presentation routes must not perform direct external HTTP I/O. Put network clients behind application-layer ports and infrastructure adapters.
- `runtime_app.py` should compose runtime modules; process loops, subprocess lifecycle, and scheduler implementations belong in `opennamu_forge/presentation/runtime/`.
- `runtime_app.py` should install route registration through `opennamu_forge.presentation.route_registry.register_routes`; direct `app.route(...)` blocks belong in the route registry.
- Presentation routes must not use raw SQL or `db_change()` directly.
- Do not reintroduce `get_db_connect()` or `opennamu_forge/presentation/shared/db_connection.py`; DB connection/session behavior belongs in infrastructure adapters.
- Wiki setting reads belong in `WikiSettingsService`; route modules should not query the `other` table directly.
- Infrastructure repository implementations must not leak SQLModel rows to presentation/application callers.
- Network clients belong in infrastructure. Presentation may assemble request context for an adapter, but infrastructure clients must not import Flask.

## Refactor Rule

When changing an existing feature:

1. Add characterization tests or integration tests for current expected behavior.
2. Move new behavior into the appropriate `opennamu_forge/*` layer.
3. Keep existing route signatures and URLs stable.
4. Remove stale wrappers and deleted import paths in the same change.
5. Add a migration plan only when schema or public URL behavior changes.
