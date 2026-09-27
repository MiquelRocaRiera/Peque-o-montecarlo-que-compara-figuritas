import numpy as np
from PIL import Image
from area_montecarlo import estimate, foreground_mask


def test_half_black_image(tmp_path):
    a = np.full((20, 20, 3), 255, dtype=np.uint8)
    a[:, :10] = 0
    path = tmp_path / 'half.png'
    Image.fromarray(a).save(path)
    m = foreground_mask(path)
    result = estimate(m, samples=100_000, seed=1)
    assert result['exact_percentage'] == 50
    assert abs(result['percentage'] - 50) < 1


def test_seed_reproducible():
    mask = np.eye(5, dtype=bool)
    assert estimate(mask, 100, 5) == estimate(mask, 100, 5)
