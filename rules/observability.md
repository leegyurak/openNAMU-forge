# 관측 가능성

Prometheus metric은 `prometheus-flask-exporter`를 통해 `/metrics`로 노출됩니다.

## 규칙

- `/metrics`는 기본 scrape endpoint로 유지합니다.
- OpenNamu Forge application metadata metric은 `opennamu_forge_*` prefix를 사용합니다.
- Prometheus 설정은 `.env`의 `NAMU_PROMETHEUS_ENABLED`, `NAMU_PROMETHEUS_PATH`, `NAMU_PROMETHEUS_GROUP_BY`를 따릅니다.
- cookie, IP, password, document content, raw username 같은 민감 정보는 metric label에 넣지 않습니다.
- endpoint, method, status, runtime version, DB type처럼 cardinality가 낮은 label을 사용합니다.
- per-document, per-user, per-IP label을 추가하지 않습니다.
- background job metric을 추가할 때도 label set이 bounded인지 확인합니다.
- metric route나 label 정책을 바꾸면 `.env.example`, README, Docker docs, monitoring tests를 같이 갱신합니다.
