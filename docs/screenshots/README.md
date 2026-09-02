# Screenshot capture guide

Run the stack with Docker Compose and capture only synthetic/demo content. Do not include patient data, credentials, browser profiles, terminal history, or local file paths.

Suggested screenshots:

1. `dashboard.png` — initial dashboard and upload control.
2. `viewer.png` — uploaded synthetic slide with an active zoomed viewport.
3. `analysis.png` — experimental analysis/heatmap result.
4. `scanner.png` — scanner progress received through the WebSocket connection.

Save images in this directory and reference them from the top-level README with relative links, for example:

```md
![MicroSight viewer](docs/screenshots/viewer.png)
```

Verify screenshots contain no private or diagnostic data before committing them.

diff --git a/LICENSE b/LICENSE
