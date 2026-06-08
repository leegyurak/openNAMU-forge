# Testing and Coverage

## Baseline Commands

```bash
uv run --extra dev pytest
uv run --extra dev pytest tests/integration
uv run --extra dev python -m coverage run -m pytest
uv run --extra dev python -m coverage report --fail-under=90
```

## Coverage Target

Maintain at least 90% test coverage for new or substantially changed Python code.

If a full-app coverage run is not practical because importing `app.py` starts DB bootstrap and GopenNAMU, measure the isolated module or package under change and document any excluded integration path.

## Test Design

- Add focused tests under `tests/`.
- Integration tests live under `tests/integration/`.
- Tests are pytest-based. Do not add new `unittest.TestCase` tests.
- Test functions must use Korean names while keeping the `test_` prefix so pytest discovery works.
- Test case matrices must use `pytest.mark.parametrize`.
- Do not use explicit `for` loops, `while` loops, list/set/dict comprehensions, or generator expressions in test files. If multiple cases are needed, parametrize them.
- Prefer tests that can run without booting `app.py`, opening a DB, or starting GopenNAMU.
- For DB compatibility work, test SQL translation and SQLModel configuration separately from full integration tests.
- Keep tests deterministic and independent of network access.
- For frontend layout changes, add responsive invariant tests that protect mobile, tablet, and desktop behavior.
- Clean generated `__pycache__`, coverage databases, and local DB artifacts before finalizing changes.

## Current Test Gaps

- PostgreSQL real-DB integration tests.
- Full `app.py` boot tests with controlled DB and GopenNAMU lifecycle.
- Docker Compose smoke tests.
- Full Alembic downgrade and multi-revision upgrade path tests.
