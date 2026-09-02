# Performance

Run `python scripts/benchmark_tiles.py` after starting the backend. It prints real metrics from `/api/metrics/`, including aggregate request counts, cache ratio, and observed mean tile-request duration. `make scanner-test` builds the C++17 simulator and runs CTest. Results are intentionally not committed because this project does not fabricate benchmark values.
