# Scanner protocol

The C++17 scanner simulator has `DISCONNECTED`, `IDLE`, `MOVING`, `FOCUSING`, `CAPTURING`, `ERROR`, `COMPLETED`, and terminal `FAILED` states. A normal tile follows `IDLE → MOVING → FOCUSING → CAPTURING → IDLE`. Capture failures retry with exponential backoff; exhausted retries transition to `FAILED`. `--fail-focus` and `--fail-camera` produce deterministic failures. Standard-library mutexes protect state, and the compact controller code uses timed operations to model asynchronous hardware boundaries.

`BACKEND_URL` enables best-effort HTTP JSON callbacks to `POST /api/scanner/events/`. The simulator invokes `curl`, rather than embedding a C++ HTTP dependency; unreachable callbacks are logged and scanning continues where possible.
