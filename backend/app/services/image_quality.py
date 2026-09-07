import numpy as np

def compute_image_quality(img_array: np.ndarray) -> float:
    """
    Image Quality Gating via Laplacian variance.
    Computes sharpness using discrete 2D Laplacian operator.
    Values < BLUR_THRESHOLD (50.0) indicate blurred or degraded photographs.
    """
    if img_array is None or img_array.size == 0:
        return 0.0
        
    # Ignore alpha channel if present, average RGB channels to grayscale
    gray = np.mean(img_array[..., :3], axis=2) if img_array.ndim == 3 else img_array
    gray = gray.astype(np.float32)
    
    if gray.shape[0] < 3 or gray.shape[1] < 3:
        return 0.0

    # 2D discrete Laplacian finite difference strictly on interior pixels (eliminates toroidal edge wrap)
    laplacian = (
        gray[:-2, 1:-1] + gray[2:, 1:-1] +
        gray[1:-1, :-2] + gray[1:-1, 2:] - 4 * gray[1:-1, 1:-1]
    )
    return float(np.var(laplacian))
