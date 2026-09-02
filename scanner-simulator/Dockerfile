FROM gcc:14 AS build
RUN apt-get update && apt-get install -y --no-install-recommends cmake curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN rm -rf build && cmake -S . -B build && cmake --build build
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=build /app/build/microsight_scanner /usr/local/bin/microsight_scanner
CMD ["microsight_scanner", "--demo"]
