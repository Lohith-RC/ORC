import numpy as np
from app.services.image_quality import compute_image_quality

def test_uniform_image_has_zero_laplacian_variance():
    # Completely flat gray image has no edges/sharpness
    flat_image = np.ones((100, 100, 3), dtype=np.uint8) * 128
    score = compute_image_quality(flat_image)
    assert score == 0.0

def test_high_contrast_pattern_has_high_sharpness():
    # Checkerboard image with stark transitions produces high Laplacian variance
    checkerboard = np.zeros((100, 100, 3), dtype=np.uint8)
    checkerboard[::2, ::2] = 255
    checkerboard[1::2, 1::2] = 255
    score = compute_image_quality(checkerboard)
    assert score > 50.0  # Above BLUR_THRESHOLD

def test_empty_or_none_image():
    assert compute_image_quality(None) == 0.0
    assert compute_image_quality(np.array([])) == 0.0
