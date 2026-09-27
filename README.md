# Monte Carlo image area estimator

Estimate how much of a white-background image is occupied by a darker object. Built from a university exercise comparing small collectible figurines.

## Run

```bash
python -m pip install -r requirements.txt
python area_montecarlo.py image1.png image2.jpg --samples 100000 --threshold 245 --seed 42
python -m pytest -q
```

For each image, the tool reports the Monte Carlo occupancy, an approximate 95% sampling interval, and an exact pixel-count reference. Sampling uses independent uniformly distributed pixel positions and a reproducible seed. A pixel is foreground if **any** RGB channel is below the threshold; transparency is placed over white. The reference count helps verify the simulation.

**Interpretation:** Percentages describe the share of each image canvas. For meaningful comparisons, photograph objects at the same scale, orientation, lighting and crop, ideally on identically sized canvases. Projected area does **not** establish mass or weight. The interval covers Monte Carlo sampling error only; thresholding and photography introduce additional uncertainty.

## Origin and improvements

The original `Programa` script remains for provenance. This version adds an explicit CLI, reproducible vectorized sampling, exact reference, sampling interval, threshold control and tests. Example image files named in the original script were not present in the repository.
