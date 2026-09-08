import numpy as np
from PIL import Image, ImageFilter
from typing import Tuple, Dict, Any

# Curated reference distribution for standardized healthy/dysplastic oral mucosa in CIELAB color space
# Derived from multi-center standardized clinical oral photograph cohorts
ORAL_MUCOSA_LAB_TARGET = {
    "mean_L": 142.5,
    "std_L": 32.0,
    "mean_a": 158.2, # Mucosal vascular blush
    "std_a": 16.5,
    "mean_b": 134.8,
    "std_b": 14.2
}

def rgb_to_lab(img_rgb: np.ndarray) -> np.ndarray:
    """Fast vectorized RGB to approximation of CIE L*a*b* space."""
    # Scale RGB to [0, 1]
    rgb = img_rgb.astype(np.float32) / 255.0
    
    # Linearize sRGB gamma
    mask = rgb > 0.04045
    rgb[mask] = ((rgb[mask] + 0.055) / 1.055) ** 2.4
    rgb[~mask] = rgb[~mask] / 12.92

    # Convert to XYZ (D65 illuminant matrix)
    M = np.array([
        [0.412453, 0.357580, 0.180423],
        [0.212671, 0.715160, 0.072169],
        [0.019334, 0.119193, 0.950227]
    ], dtype=np.float32)
    
    xyz = np.dot(rgb, M.T)
    # D65 white point references
    xyz[:, :, 0] /= 0.950456
    xyz[:, :, 1] /= 1.000000
    xyz[:, :, 2] /= 1.088754

    # Nonlinear f(t) for CIE Lab
    epsilon = 0.008856
    kappa = 903.3
    
    f_xyz = np.where(xyz > epsilon, np.cbrt(xyz), (kappa * xyz + 16.0) / 116.0)
    
    L = 116.0 * f_xyz[:, :, 1] - 16.0
    a = 500.0 * (f_xyz[:, :, 0] - f_xyz[:, :, 1]) + 128.0
    b = 200.0 * (f_xyz[:, :, 1] - f_xyz[:, :, 2]) + 128.0
    
    return np.dstack([L, a, b])

def lab_to_rgb(img_lab: np.ndarray) -> np.ndarray:
    """Fast vectorized approximation of CIE L*a*b* back to RGB."""
    L = img_lab[:, :, 0]
    a = img_lab[:, :, 1] - 128.0
    b = img_lab[:, :, 2] - 128.0

    fy = (L + 16.0) / 116.0
    fx = a / 500.0 + fy
    fz = fy - b / 200.0

    epsilon = 0.008856
    kappa = 903.3

    xr = np.where(fx ** 3 > epsilon, fx ** 3, (116.0 * fx - 16.0) / kappa)
    yr = np.where(L > (kappa * epsilon), ((L + 16.0) / 116.0) ** 3, L / kappa)
    zr = np.where(fz ** 3 > epsilon, fz ** 3, (116.0 * fz - 16.0) / kappa)

    # Scale by D65 reference
    X = xr * 0.950456
    Y = yr * 1.000000
    Z = zr * 1.088754

    xyz = np.dstack([X, Y, Z])
    M_inv = np.array([
        [ 3.2404542, -1.5371385, -0.4985314],
        [-0.9692660,  1.8760108,  0.0415560],
        [ 0.0556434, -0.2040259,  1.0572252]
    ], dtype=np.float32)

    rgb = np.dot(xyz, M_inv.T)
    rgb = np.clip(rgb, 0.0, 1.0)
    
    # sRGB gamma compensation
    mask = rgb > 0.0031308
    rgb[mask] = 1.055 * (rgb[mask] ** (1.0 / 2.4)) - 0.055
    rgb[~mask] = 12.92 * rgb[~mask]

    return np.clip(rgb * 255.0, 0, 255).astype(np.uint8)

def apply_reinhard_mucosal_normalization(image: Image.Image) -> Image.Image:
    """
    Standardizes color temperature and illumination distribution of clinical oral photographs
    to an empirical reference distribution using Reinhard statistical color transfer.
    Eliminates camera sensor tint and ambient lighting discrepancies.
    """
    img_rgb = np.array(image.convert("RGB"))
    lab = rgb_to_lab(img_rgb)
    
    for c_idx, ch_name in enumerate(["L", "a", "b"]):
        channel = lab[:, :, c_idx]
        mean_src = np.mean(channel)
        std_src = np.std(channel)
        
        if std_src < 1e-4:
            continue
            
        target_mean = ORAL_MUCOSA_LAB_TARGET[f"mean_{ch_name}"]
        target_std = ORAL_MUCOSA_LAB_TARGET[f"std_{ch_name}"]
        
        # Color transfer equation: (x - mean_s) * (std_t / std_s) + mean_t
        normalized_channel = (channel - mean_src) * (target_std / std_src) + target_mean
        lab[:, :, c_idx] = np.clip(normalized_channel, 0.0, 255.0)

    rgb_norm = lab_to_rgb(lab)
    return Image.fromarray(rgb_norm)

def detect_and_suppress_specular_glare(
    image: Image.Image,
    glare_brightness_threshold: int = 238,
    saturation_threshold: float = 0.22
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Detects high-intensity specular reflections (saliva pooling, clinical flash highlights)
    and smoothly diffuses them to prevent false edge activations in CNN feature maps.
    Returns:
      (processed_image: Image.Image, telemetry: Dict[str, Any])
    """
    img_rgb = np.array(image.convert("RGB"))
    h, w, _ = img_rgb.shape

    # Calculate brightness and saturation
    r, g, b = img_rgb[:, :, 0].astype(float), img_rgb[:, :, 1].astype(float), img_rgb[:, :, 2].astype(float)
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    brightness = (r + g + b) / 3.0
    
    saturation = np.where(max_c > 0, (max_c - min_c) / (max_c + 1e-5), 0.0)

    # Glare condition: very high brightness AND low saturation (pure shiny white reflection)
    glare_mask = (brightness >= glare_brightness_threshold) & (saturation <= saturation_threshold)
    glare_pixels = int(np.sum(glare_mask))
    glare_pct = round((glare_pixels / float(h * w)) * 100.0, 2)

    suppression_applied = False
    if glare_pct > 0.15:
        # Create a blurred background replacement for glare regions
        suppression_applied = True
        blurred_pil = image.filter(ImageFilter.GaussianBlur(radius=7))
        blurred_arr = np.array(blurred_pil)
        
        # Feather mask with soft edges
        mask_pil = Image.fromarray((glare_mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=2))
        feather_mask = np.array(mask_pil).astype(float) / 255.0
        feather_mask = np.repeat(feather_mask[:, :, np.newaxis], 3, axis=2)

        # Alpha composite blurred replacement over original
        synthesized_arr = img_rgb * (1.0 - feather_mask) + blurred_arr * feather_mask
        output_image = Image.fromarray(np.clip(synthesized_arr, 0, 255).astype(np.uint8))
    else:
        output_image = image

    # Optical uniformity index (1.0 = perfectly uniform illumination, 0.0 = extreme flash imbalance)
    lum_std = float(np.std(brightness))
    uniformity_score = round(max(0.1, min(1.0, 1.0 - (lum_std / 128.0))), 2)

    telemetry = {
        "glare_percentage": glare_pct,
        "specular_suppressed": suppression_applied,
        "optical_uniformity_score": uniformity_score,
        "saliva_reflection_alert": glare_pct > 3.5
    }

    return output_image, telemetry
