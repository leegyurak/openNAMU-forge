# Repository and DTO Rules

Repositories are infrastructure adapters. They must stay thin, deterministic, and isolated from presentation concerns.

## Interfaces

- Every repository capability used outside infrastructure must have an application-layer protocol in `opennamu_forge/application/ports/`.
- Presentation and application code should type against ports, not concrete repository classes.
- Factory helpers may instantiate concrete repositories, but their return type should be the corresponding port.

## DTO and Mapper Boundary

- Repository methods must return DTOs or scalar primitives, never SQLModel row objects.
- DTOs live in `opennamu_forge/application/dto/`.
- Mapper functions live near the concrete adapter under `opennamu_forge/infrastructure/mappers/`.
- Mapping from SQLModel row to DTO must happen in mapper functions, not in route code.

## Settings

- Setting keys must be represented by `SettingKey` under `opennamu_forge/application/dto/settings.py`.
- Presentation code should read wiki settings through `WikiSettingsService`, not by hardcoding `other.name` SQL in routes.
- Dynamic setting names are allowed only when the route validates the name against a local allow-list first, such as skin setting keys; use `WikiSettingsService.get_dynamic()` for those cases.
- Adding a new runtime/wiki setting requires updating `SettingKey`, `.env.example` when environment-backed, and the related tests/docs.

## Repository Control Flow

- Repository files must not contain explicit `if`, `for`, or `while` statements.
- Repository files must not contain list/set/dict comprehensions or generator expressions.
- Express filtering and conditional behavior as SQL expressions such as `where`, `case`, `coalesce`, `exists`, `delete`, `update`, or `merge`.
- Bulk writes should use SQLAlchemy/SQLModel session capabilities or mapper-prepared data; do not hand-roll loops in repository methods.

## Type Conversion

- Do not wrap ORM result collections with `list()` just to satisfy typing.
- Use `typing.cast` for static typing when SQLAlchemy/SQLModel result typing is narrower at runtime than ty can infer.

## Tests

- Add tests for repository contracts and mapper behavior before changing route behavior.
- Add convention tests that prevent repository control-flow regressions.
