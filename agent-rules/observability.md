# Observability

Prometheus metrics are exposed at `/metrics` through `prometheus-flask-exporter`.

## Rules

- Keep `/metrics` available for Prometheus scraping.
- Keep OpenNamu Forge application metadata under the `opennamu_forge_*` metric prefix.
- Prometheus can be customized through `.env`: `NAMU_PROMETHEUS_ENABLED`, `NAMU_PROMETHEUS_PATH`, and `NAMU_PROMETHEUS_GROUP_BY`.
- Avoid putting sensitive request data, cookies, IP addresses, passwords, or document content into metric labels.
- Prefer low-cardinality labels such as endpoint, method, status, runtime version, and DB type.
- Do not add per-document, per-user, or per-IP labels.
- When adding background jobs, expose counters or gauges only if labels remain bounded.
