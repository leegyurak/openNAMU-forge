# 저장소와 DTO 규칙

Repository는 infrastructure adapter입니다. Presentation 관심사와 분리하고, 얇고 결정적으로 유지합니다.

## Interface

- Infrastructure 밖에서 쓰는 repository capability는 `opennamu_forge/application/ports/` protocol을 가져야 합니다.
- Presentation/Application code는 concrete repository class보다 port에 type을 맞춥니다.
- Factory/provider는 concrete repository를 만들 수 있지만 return type은 port로 둡니다.

## DTO와 Mapper

- Repository method는 DTO나 scalar primitive만 반환합니다.
- SQLModel row object를 presentation/application으로 넘기지 않습니다.
- DTO는 `opennamu_forge/application/dto/`에 둡니다.
- Mapper는 `opennamu_forge/infrastructure/mappers/`에 둡니다.
- SQLModel row to DTO 변환은 mapper에서 하고 route code에서 하지 않습니다.
- Mapper batch conversion은 row-to-DTO/model 변환 목적일 때만 comprehension을 허용합니다.

## Settings

- `settings`는 wiki/user/domain behavior에만 사용합니다.
- `.env`, DB connection, pool, Prometheus, Gunicorn, startup option은 `config`입니다.
- setting key는 `opennamu_forge/application/dto/settings.py`의 `SettingKey`를 우선 사용합니다.
- route에서 dynamic setting name을 받을 때는 local allow-list로 검증한 뒤 `WikiSettingsService.get_dynamic()` 같은 경계를 사용합니다.
- 새 wiki/user setting은 `SettingKey`, service/repository test, 관련 docs를 같이 갱신합니다.

## Repository Control Flow

- Repository file에는 명시적 `if`, `for`, `while`을 넣지 않습니다.
- Repository file에는 list/set/dict comprehension, generator expression을 넣지 않습니다.
- Filtering과 conditional behavior는 SQLAlchemy/SQLModel expression으로 표현합니다.
- Optional filter를 `or_(literal(not flag), condition)` 같은 SQL tautology로 표현하지 않습니다.
- 동적 filter 조합은 JPA Specification에 대응하는 작은 query spec/composer로 조립합니다.
  - 예: `WikiTitleSpec.from_exclusions(...).criteria(title_column)`
  - 예: `BacklinkRedirectSpec.title_or_link(...).criteria(...)`
  - spec/composer는 infrastructure 안에 두고, route/application port는 기존 DTO/scalar 계약을 우선 유지합니다.
- 두 개 이상의 조건을 `or_(...)`로 조합하는 query fragment도 repository 본문에 두지 않고 spec/composer로 위임합니다.
- Bulk write는 SQLAlchemy/SQLModel session 기능이나 mapper-prepared data를 사용합니다.
- ORM result를 typing 때문에 `list()`로 감싸지 않습니다. 필요하면 `typing.cast`를 사용합니다.
- `*_by_title_type`처럼 이름에 조건 컬럼이 드러나는 repository method는 method name과 `where(...)` equality 조건이 어긋나지 않게 유지합니다.

## 테스트

- repository contract test와 mapper test를 먼저 추가합니다.
- convention test는 repository control-flow regression을 막아야 합니다.
- convention test는 repository 본문의 직접 `or_`, optional-filter SQL tautology, 대표적인 `by_X_Y` method의 where-condition mismatch를 막아야 합니다.
- route behavior 변경은 repository/application 경계를 검증한 뒤 진행합니다.
