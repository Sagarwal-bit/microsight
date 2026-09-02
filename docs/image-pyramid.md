# Image pyramid

Loading a full-resolution slide in a browser wastes bandwidth and memory. MicroSight uses 256×256 JPEG tiles. Level 0 is the smallest image and each next level doubles in resolution until source size. `GET /api/slides/{id}/tiles/{level}/{x}/{y}/` validates all coordinates and returns a cached tile with a five-minute cache header. Edge crops retain their natural smaller dimensions.

The React viewer converts viewport bounds through its pan/zoom transform into source-image coordinates, selects `floor(maxLevel + log2(zoom))`, divides the result by the source-space tile size, and requests the bounded `(x,y)` range plus a one-tile margin. React renders one keyed item per coordinate/level URL, preventing duplicate tile requests per viewport update. The API cache is bounded by the configured cache backend.
