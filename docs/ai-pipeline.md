# AI pipeline

`BaselineCV` computes grayscale darkness and Laplacian texture per analysis window to produce experimental region flags, then applies Otsu thresholding and connected components for object-like blobs. Quality metrics are numeric heuristics (brightness, contrast, focus variance, saturation, clipped-pixel artifact fraction). No model is downloaded, no accuracy is claimed, and no output is a diagnosis. A replaceable ML engine can later implement the same region/object contract.
