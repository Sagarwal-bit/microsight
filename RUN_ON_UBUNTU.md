# Run MicroSight on Ubuntu

## Prerequisites

Install Docker Engine with the Docker Compose plugin. Docker Desktop is optional on Ubuntu. Verify:

```bash
docker --version
docker compose version
```

## Start the complete stack

From the extracted project folder:

```bash
cp .env.example .env
docker compose --env-file .env up --build
```

Open `http://localhost:4200`. The Django API is available on `http://localhost:8000/api/health/`.

## Create demo data

In another terminal, with Python 3 plus Pillow/NumPy/OpenCV installed:

```bash
python3 scripts/generate_demo_image.py
```

Upload the resulting `work/demo-microscopy.png` through the browser.

## Validation commands

```bash
docker compose --env-file .env run --rm backend python manage.py migrate --run-syncdb
docker compose --env-file .env run --rm backend python manage.py test
cmake -S scanner-simulator -B scanner-simulator/build
cmake --build scanner-simulator/build
ctest --test-dir scanner-simulator/build --output-on-failure
python3 scripts/benchmark_tiles.py
```

## Stop services

```bash
docker compose down
```

To also remove the local MySQL data volume:

```bash
docker compose down -v
```
