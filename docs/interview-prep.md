# Interview preparation

## Stack answers

**Why React, not Angular?** React keeps this migration small: components and hooks cover viewer state, upload state, and scanner WebSocket state without a separate state library. TypeScript prevents mismatches with Django contracts. Angular would also be suitable, but React better matches the final stack requested for this project. The viewer derives tiles from zoom, viewport and `(x,y)`, uses stable keys, and requests only visible tiles plus one margin.

**Why Django, DRF and Channels?** Django supplies models and secure upload handling; DRF validates API input; Channels relays persisted scanner events over WebSockets. Malformed events return 400. If Redis fails, the service can use its in-memory fallback locally, but multi-instance real-time delivery is degraded.

**Why MySQL?** MicroSight metadata is relational: slides own jobs, regions, annotations, objects and scanner events. Foreign keys maintain those relationships; indexes serve slide/status and slide/score reads. Images remain filesystem objects because MySQL is not a tile object store. Concurrent writes are transactional database writes, with Django responsible for validation and transaction boundaries.

**Why Redis?** Frequent tile reads are cacheable and Channels needs a lightweight message layer. MySQL is durable metadata storage, not a low-latency tile cache. Cache loss causes a safe disk read, not data loss.

**Why pyramids and tiles?** A viewer maps viewport pixels through pan/zoom into source-image bounds, selects a suitable downsampled level, then divides bounds by 256 to find `(x,y)` tiles. Origin is upper-left; x increases right and y downward. Edge tiles are smaller crops. Pyramids avoid transferring the full image.

**Why C++17?** The C++ scanner simulator demonstrates state machines, mutex-protected shared state, timing, retries and backoff close to a performance-sensitive hardware boundary. Python would be simpler but would not demonstrate that boundary; Java is deliberately not part of the final stack. A failed callback never crashes scanning.

**Scaling:** use separate API instances, workers for pyramid/analysis, object storage for huge images, a CDN/cache for tiles, and observability around request latency, cache rate, queue time and scanner failures. Baseline CV output remains experimental—not clinically validated.
