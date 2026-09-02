# API

- `POST/GET /api/slides/` upload/list.
- `GET /api/slides/{id}/tiles/{level}/{x}/{y}/` fetch a JPEG tile.
- `POST /api/slides/{id}/analyze/`, `quality-check/`; `GET heatmap/`, `objects/`.
- `GET/POST /api/annotations/slides/{id}/annotations/`; standard CRUD `/api/annotations/{id}/`.
- `POST /api/scanner/events/`, `GET /api/scanner/jobs/`, `GET /api/health/`, `GET /api/metrics/`.
