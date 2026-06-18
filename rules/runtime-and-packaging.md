# 런타임과 패키징

## Runtime Stack

- Python 3.10+ 호환성을 유지합니다.
- Flask 3.1+ async route를 사용합니다.
- 운영 WSGI server는 Gunicorn입니다.
- package manager와 command runner는 `uv`입니다.
- Docker image는 `uv sync --frozen`으로 dependency를 설치합니다.

## Config Naming

- `.env`, CLI flag, DB connection, engine pool, Prometheus, Gunicorn, process startup 값은 `config`입니다.
- wiki/user/domain behavior 값은 `settings`입니다.
- Runtime config builder는 `DatabaseConfig`, `MonitoringConfig` 같은 typed config object를 반환합니다.
- historical dictionary shape가 필요하면 `DatabaseConfig.to_database_options()` 같은 명시 boundary에서만 변환합니다.

## uv Workflow

개발 설치:

```bash
uv sync --extra performance --extra dev
```

runtime-only 설치:

```bash
uv sync --frozen --no-dev --extra performance
```

실행:

```bash
uv run python -m opennamu_forge.cli migrate
uv run python -m opennamu_forge.cli dev
uv run python -m opennamu_forge.cli serve --host 0.0.0.0 --port 3000 --workers 1 --threads 1
```

dependency 변경:

```bash
uv lock
```

`requirements.txt`, runtime dependency installer, OS별 shell/batch wrapper를 추가하지 않습니다.

## Runtime Boundary

- `runtime_app.py`는 runtime 조립을 담당하고 얇게 유지합니다.
- process loop, GopenNAMU lifecycle, scheduler, restart/shutdown primitive, startup task는 `opennamu_forge/presentation/runtime/` 아래에 둡니다.
- route handler는 restart/shutdown 화면을 authorize/render할 수 있지만 직접 `subprocess.Popen`, `os._exit`, `sys.exit`, restart thread를 호출하지 않습니다.
- HTTP handler가 git remote를 바꾸거나, hard reset하거나, release archive를 project tree에 내려받거나, source file을 덮어쓰는 기능을 추가하지 않습니다.

## Python Style

- Python 3.10 호환 typing을 사용합니다.
- 구조가 명확해질 때만 structural pattern matching을 사용합니다.
- infrastructure/runtime 경계에는 작고 typed helper를 선호합니다.
- route code를 문법 현대화 목적으로만 넓게 다시 쓰지 않습니다.

## 품질 명령

```bash
uv run --extra dev ruff check app.py opennamu_forge migrations tests opennamu_forge/presentation/shared/sql_dialect.py
uv run --extra dev ty check app.py opennamu_forge/config opennamu_forge/application opennamu_forge/infrastructure opennamu_forge/presentation/flask_factory.py opennamu_forge/presentation/theme.py opennamu_forge/presentation/__init__.py opennamu_forge/presentation/url_converters.py opennamu_forge/presentation/dependencies.py opennamu_forge/presentation/response_helpers.py opennamu_forge/presentation/encoding_helpers.py opennamu_forge/presentation/captcha_helpers.py opennamu_forge/presentation/email_helpers.py opennamu_forge/presentation/file_helpers.py opennamu_forge/presentation/authorization_helpers.py opennamu_forge/presentation/identity_helpers.py opennamu_forge/presentation/text_helpers.py opennamu_forge/presentation/user_validation_helpers.py opennamu_forge/presentation/route_registry.py opennamu_forge/presentation/runtime migrations tests
```
