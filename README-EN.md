[(en-US)](./README-EN.md) | [(ko-KR)](./README.md)

# OpenNamu Forge
[![Python](https://img.shields.io/badge/python->=%203.10-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1+-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-UI-61DAFB.svg?logo=react&logoColor=222222)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-typed-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](./rules/testing-and-coverage.md)
[![Open Source](https://img.shields.io/badge/open%20source-yes-brightgreen.svg)](./LICENSE)
[![LICENSE](https://img.shields.io/badge/license-BSD%203--Clause-lightgrey.svg)](./LICENSE)

![](https://raw.githubusercontent.com/openNAMU/openNAMU/beta/.github/logo.png)

OpenNamu Forge is a modernized, agent-friendly Python/Flask wiki engine based on openNAMU.

## Quick Start

```bash
cp .env.example .env
uv sync --extra performance --extra dev
uv run python -m opennamu_forge.cli migrate
uv run python -m opennamu_forge.cli dev
```

Set `NAMU_THEME_COLOR` in `.env` to customize the primary UI color. Hex colors such as `#00a495` are supported.

Production-style local WSGI:

```bash
uv run python -m opennamu_forge.cli serve --host 0.0.0.0 --port 3000 --workers 1 --threads 1
```

## Clone
You can clone this repository by entering the following command at the terminal (command prompt):
 * `git clone https://github.com/<your-org>/opennamu-forge.git`

## Contribute
OpenNamu Forge inherits openNAMU's wiki engine behavior and adds a modern runtime, PostgreSQL/SQLModel foundations, pytest coverage, observability, and agent-oriented contribution rules.

The upstream openNAMU project remains available for original issues and pull requests. [(Create Issues)](https://github.com/openNAMU/openNAMU/issues/new)

## Documentation

- [AGENTS.md](./AGENTS.md): agent workflow rules
- [docs/docker.md](./docs/docker.md): Docker and Docker Compose guide
- [rules/runtime-and-packaging.md](./rules/runtime-and-packaging.md): runtime, uv, CLI, Ruff, and ty rules
- [rules/database-and-migrations.md](./rules/database-and-migrations.md): DB, SQLModel, and Alembic rules
- [rules/testing-and-coverage.md](./rules/testing-and-coverage.md): pytest and coverage rules
- [skills/](./skills/): task playbooks

## License
OpenNamu Forge follows the upstream [BSD 3-Clause License](./LICENSE). Please refer to the documentation for details.

### External Projects
 * [Quotes icon - Dave Gandy](http://www.flaticon.com/free-icon/quote-left_25672)
 * [highlight.js](https://highlightjs.org/)
 * [KaTeX](https://katex.org/)
 * [Feather](https://feathericons.com/)
 * [GopenNAMU](https://github.com/openNAMU/GopenNAMU)

## Etc.
 * Owner rights are granted to the first registor.
 * [Test Server](http://2du.pythonanywhere.com)
 * [Contributors](https://github.com/openNAMU/openNAMU/graphs/contributors)
