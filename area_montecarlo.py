"""Estimate foreground occupancy of white-background images with Monte Carlo sampling."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps


def foreground_mask(path: str | Path, threshold: int = 245) -> np.ndarray:
    """Pixels with any RGB channel below threshold are foreground; alpha is composited on white."""
    if not 0 <= threshold <= 255:
        raise ValueError("threshold must be between 0 and 255")
    with Image.open(path) as source:
        source = ImageOps.exif_transpose(source).convert("RGBA")
        background = Image.new("RGBA", source.size, (255, 255, 255, 255))
        rgb = np.asarray(Image.alpha_composite(background, source).convert("RGB"))
    return np.any(rgb < threshold, axis=2)


def estimate(mask: np.ndarray, samples: int = 100_000, seed: int = 42) -> dict:
    if mask.ndim != 2 or mask.size == 0 or samples <= 0:
        raise ValueError("Expected a nonempty 2D mask and positive samples")
    height, width = mask.shape
    rng = np.random.default_rng(seed)
    rows = rng.integers(0, height, size=samples)
    cols = rng.integers(0, width, size=samples)
    p = float(mask[rows, cols].mean())
    se = np.sqrt(p * (1 - p) / samples)
    return {"fraction": p, "percentage": 100 * p,
            "pixels_estimated": p * mask.size,
            "ci95_percentage": [100 * max(0, p - 1.96 * se), 100 * min(1, p + 1.96 * se)],
            "exact_percentage": 100 * float(mask.mean()), "width": width, "height": height}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--samples", type=int, default=100_000)
    parser.add_argument("--threshold", type=int, default=245)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    results = []
    for path in args.images:
        result = estimate(foreground_mask(path, args.threshold), args.samples, args.seed)
        results.append((path, result))
    for path, r in sorted(results, key=lambda item: item[1]["percentage"], reverse=True):
        lo, hi = r["ci95_percentage"]
        print(f"{path}: {r['percentage']:.2f}% (95% approx. CI {lo:.2f}–{hi:.2f}%), "
              f"exact {r['exact_percentage']:.2f}%, image {r['width']}×{r['height']}")


if __name__ == "__main__":
    main()
