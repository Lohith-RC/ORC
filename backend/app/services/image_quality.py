import numpy as np

def compute_image_quality(img_array: np.ndarray) -> float:
    """
    Image Quality Gating via Laplacian variance.
    Computes sharpness using discrete 2D Laplacian operator.
    Values < BLUR_THRESHOLD (50.0) indicate blurred or degraded photographs.
    """
    if img_array is None or img_array.size == 0:
        return 0.0
        
    gray = np.mean(img_array, axis=2) if img_array.ndim == 3 else img_array
    gray = gray.astype(np.float32)
    
    # 2D discrete Laplacian finite difference
    laplacian = (
        np.roll(gray, -1, 0) + np.roll(gray, 1, 0) +
        np.roll(gray, -1, 1) + np.roll(gray, 1, 1) - 4 * gray
    )
    return float(np.var(laplacian))
