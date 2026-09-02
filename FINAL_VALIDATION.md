# Validation record

Validation is performed in the target environment; do not treat this file as a substitute for running the commands below after cloning.

## Commands

```bash
cp .env.example .env
docker compose --env-file .env config
docker compose --env-file .env up --build
python3 scripts/generate_demo_image.py
docker compose --env-file .env run --rm backend python manage.py test
cmake -S scanner-simulator -B scanner-simulator/build
cmake --build scanner-simulator/build
ctest --test-dir scanner-simulator/build --output-on-failure
python3 -m compileall -q backend scripts
python3 scripts/benchmark_tiles.py
```

## Current release checks

- React production build completed with `npm run build`.
- C++ scanner CTest suite passed.
- Django backend tests passed when run with a local database administrator account that can create the temporary test database.
- Docker Compose configuration rendered successfully.
- The running stack served the frontend and a healthy API response with MySQL and Redis configured.

## Known limitations
