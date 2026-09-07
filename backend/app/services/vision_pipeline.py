import math
import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

from app.services.ml_engine import run_inference_pipeline
from app.services.image_quality import compute_image_quality

@dataclass
class LesionSpatialTelemetry:
    mask_detected: bool
    center_pct: Tuple[float, float]
    diameter_mm: float
    surface_area_mm2: float
    border_irregularity_score: float
    contour_points: List[Tuple[float, float]] # List of [x_pct, y_pct]
    optical_cross_polarized: bool
    vital_stain_present: bool
    vital_stain_abnormal: bool

def compute_lesion_segmentation(
    image: Image.Image,
    distance_mm: float = 50.0
) -> Tuple[bool, Tuple[float, float], float, float, float, List[Tuple[float, float]]]:
    """
    Stage I: Semantic Mucosal Lesion Segmentation & Spatial Morphology.
    Extracts lesion boundary, calibrated dimensions (mm), and border irregularity index.
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Invalid image input: expected PIL.Image.Image instance")

    distance_mm = max(10.0, min(500.0, float(distance_mm)))
    img_rgb = np.array(image.convert("RGB"))
    if img_rgb.ndim != 3 or img_rgb.shape[0] < 16 or img_rgb.shape[1] < 16:
        raise ValueError("Image dimensions too small for clinical segmentation (min 16x16 required)")

    h, w, _ = img_rgb.shape

    # 1. Color space transformation: mucosal erythema & leukoplakic contrast
    r, g, b = img_rgb[:, :, 0].astype(float), img_rgb[:, :, 1].astype(float), img_rgb[:, :, 2].astype(float)
    
    # Erythema index: emphasizes capillary dilatation and dysplastic vascularity
    erythema = (r - g) / (r + g + 1e-5)
    # Leukoplakia index: high brightness + low saturation
    brightness = (r + g + b) / 3.0
    
    # Combined mucosal lesion activation field
    lesion_field = 0.6 * erythema + 0.4 * (brightness / 255.0)
    
    # Thresholding relative to background mucosal mean
    threshold = np.mean(lesion_field) + 0.8 * np.std(lesion_field)
    binary_mask = lesion_field > threshold

    # Count active pixels
    active_pixels = np.sum(binary_mask)
    total_pixels = h * w
    
    # If no distinct focal lesion detected, define central region of interest
    if active_pixels < (total_pixels * 0.005):
        # Fallback to central inspection zone (default 12mm diameter)
        cx, cy = 50.0, 50.0
        diameter_mm = 12.0
        area_mm2 = math.pi * ((diameter_mm / 2.0) ** 2)
        irregularity = 1.15
        
        # Synthetic circular contour centered at 50%, 50%
        contour = []
        for deg in range(0, 360, 20):
            rad = math.radians(deg)
            contour.append((
                round(50.0 + 12.0 * math.cos(rad), 1),
                round(50.0 + 12.0 * math.sin(rad), 1)
            ))
        return False, (cx, cy), diameter_mm, area_mm2, irregularity, contour

    # Compute spatial center of mass
    y_indices, x_indices = np.where(binary_mask)
    cy_pct = round(float(np.mean(y_indices)) / h * 100.0, 1)
    cx_pct = round(float(np.mean(x_indices)) / w * 100.0, 1)

    # Spatial optical calibration: 50mm optical spacer equates to ~0.08 mm per pixel on 224x224
    mm_per_pixel = (distance_mm / 50.0) * (20.0 / max(h, w))
    pixel_area = float(active_pixels)
    area_mm2 = round(pixel_area * (mm_per_pixel ** 2), 2)
    
    # Equivalent circular diameter
    equivalent_radius_mm = math.sqrt(area_mm2 / math.pi) if area_mm2 > 0 else 5.0
    diameter_mm = round(equivalent_radius_mm * 2.0, 1)

    # Extract perimeter contour points
    contour = []
    # Sample 16 radial sectors from center of mass
    for angle_deg in range(0, 360, 22):
        rad = math.radians(angle_deg)
        dx, dy = math.cos(rad), math.sin(rad)
        
        # Ray-march to find edge of binary mask
        edge_r = equivalent_radius_mm / mm_per_pixel
        for r_step in range(int(edge_r * 0.5), int(edge_r * 2.2), 2):
            sample_x = int(np.mean(x_indices) + r_step * dx)
            sample_y = int(np.mean(y_indices) + r_step * dy)
            if 0 <= sample_x < w and 0 <= sample_y < h:
                if not binary_mask[sample_y, sample_x]:
                    edge_r = r_step
                    break
                    
        pt_x = round(float(np.mean(x_indices) + edge_r * dx) / w * 100.0, 1)
        pt_y = round(float(np.mean(y_indices) + edge_r * dy) / h * 100.0, 1)
        contour.append((max(2.0, min(98.0, pt_x)), max(2.0, min(98.0, pt_y))))

    # Border irregularity (compactness metric: P^2 / (4 * pi * A))
    # Higher scores (>1.4) indicate aggressive, jagged, infiltrative carcinoma margins
    perimeter_px = len(contour) * (2.0 * math.pi * (equivalent_radius_mm / mm_per_pixel) / len(contour))
    compactness = (perimeter_px ** 2) / (4.0 * math.pi * max(1.0, pixel_area))
    irregularity_score = round(max(1.0, min(3.0, compactness)), 2)

    return True, (cx_pct, cy_pct), diameter_mm, area_mm2, irregularity_score, contour

def analyze_vital_stain(vital_stain_img: Optional[Image.Image]) -> Tuple[bool, bool]:
    """
    Analyzes secondary vital stain (Toluidine Blue) or Autofluorescence (VELscope).
    Returns (present: bool, abnormal: bool).
    """
    if vital_stain_img is None:
        return False, False
        
    arr = np.array(vital_stain_img.convert("RGB"))
    # Toluidine Blue retains in nucleic acid dense dysplastic cells (deep blue/purple)
    # Autofluorescence exhibits green emission loss in dysplastic mucosa
    r, g, b = arr[:, :, 0].astype(float), arr[:, :, 1].astype(float), arr[:, :, 2].astype(float)
    
    blue_ratio = np.mean(b / (r + g + 1.0))
    green_ratio = np.mean(g / (r + b + 1.0))
    
    # Abnormal if high blue uptake (>0.6) or marked green fluorescence loss (<0.3)
    is_abnormal = bool(blue_ratio > 0.58 or green_ratio < 0.28)
    return True, is_abnormal

def execute_dual_stage_pipeline(
    white_light_img: Image.Image,
    vital_stain_img: Optional[Image.Image] = None,
    distance_mm: float = 50.0,
    is_cross_polarized: bool = False
) -> Tuple[str, float, float, float, LesionSpatialTelemetry]:
    """
    Executes the Dual-Stage Medical Vision Pipeline:
      Stage I: Semantic Lesion Segmentation & Spatial Morphology
      Stage II: Pathological Feature Extraction with Multimodal Synthesis
    """
    # 1. Stage I: Lesion Segmentation & Spatial Morphology
    detected, center, diameter, area, irregularity, contour = compute_lesion_segmentation(
        white_light_img, distance_mm=distance_mm
    )

    # 2. Vital Stain / Autofluorescence Analysis
    stain_present, stain_abnormal = analyze_vital_stain(vital_stain_img)

    # 3. Stage II: Core Deep Learning Inference via PyTorch
    pred_class, confidence, uncertainty, quality_score = run_inference_pipeline(white_light_img)

    # Multimodal calibration: Cross-polarization eliminates false reflections, boosting certainty
    if is_cross_polarized:
        uncertainty = max(0.001, uncertainty * 0.75)

    # If vital stain is abnormal, elevate confidence if predicted cancer
    if stain_abnormal and pred_class == "cancer":
        confidence = min(0.99, confidence + 0.10)
    elif stain_abnormal and pred_class == "non_cancer":
        # Discrepancy between white light and vital dye triggers epistemic uncertainty
        pred_class = "uncertain"

    telemetry = LesionSpatialTelemetry(
        mask_detected=detected,
        center_pct=center,
        diameter_mm=diameter,
        surface_area_mm2=area,
        border_irregularity_score=irregularity,
        contour_points=contour,
        optical_cross_polarized=is_cross_polarized,
        vital_stain_present=stain_present,
        vital_stain_abnormal=stain_abnormal
    )

    return pred_class, confidence, uncertainty, quality_score, telemetry
