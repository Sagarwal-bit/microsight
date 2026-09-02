up:
	docker compose --env-file .env up --build
test:
	docker compose --env-file .env run --rm backend python manage.py test
demo:
	python scripts/generate_demo_image.py
benchmark:
	python scripts/benchmark_tiles.py
scanner-test:
	cmake -S scanner-simulator -B scanner-simulator/build
	cmake --build scanner-simulator/build
	ctest --test-dir scanner-simulator/build
