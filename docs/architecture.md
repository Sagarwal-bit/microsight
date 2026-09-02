# Architecture

React + TypeScript provides a small component-and-hooks UI with browser-safe `VITE_API_URL` and `VITE_WS_URL` configuration. Django REST validates uploads and scanner events; Channels broadcasts accepted events to a `scanner` WebSocket group. MySQL 8.4 persists relational slide, job, annotation, region, object, and event metadata. Redis is only the tile cache and Channels layer. Pillow creates disk-backed pyramids and OpenCV computes deterministic visual heuristics. The C++17 scanner simulator represents stateful, timing-sensitive hardware-like behavior without claiming to be firmware.

For scale, place API instances behind a load balancer, use worker queues for pyramid/analysis tasks, move media from local storage to object storage, and retain Redis as a bounded cache and channel layer. Celery is deliberately not part of this local prototype.
