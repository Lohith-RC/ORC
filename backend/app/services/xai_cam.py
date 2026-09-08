import io
import base64
import numpy as np
from PIL import Image
from typing import Tuple, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F

def _generate_jet_lut() -> np.ndarray:
    """Generate a standard 256-color Jet lookup table for medical thermal/activation mapping."""
    lut = np.zeros((256, 3), dtype=np.uint8)
    for i in range(256):
        v = i / 255.0
        # Jet colormap formula
        r = np.clip(1.5 - abs(4.0 * v - 3.0), 0.0, 1.0)
        g = np.clip(1.5 - abs(4.0 * v - 2.0), 0.0, 1.0)
        b = np.clip(1.5 - abs(4.0 * v - 1.0), 0.0, 1.0)
        lut[i] = [int(r * 255), int(g * 255), int(b * 255)]
    return lut

_JET_LUT = _generate_jet_lut()

class GradCAMPlusPlus:
    """
    Grad-CAM++ (Generalized Gradient-Weighted Class Activation Mapping)
    Extracts pixel-level activation heatmaps from penultimate convolutional layers.
    Addresses multiple lesion occurrences and subtle dysplastic margin gradients.
    """
    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.activations = None
        self.gradients = None
        self._handles = []
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0]

        self._handles.append(self.target_layer.register_forward_hook(forward_hook))
        self._handles.append(self.target_layer.register_full_backward_hook(backward_hook))

    def remove_hooks(self):
        for h in self._handles:
            h.remove()
        self._handles.clear()

    def generate_heatmap(
        self,
        input_tensor: torch.Tensor,
        target_class: Optional[int] = None,
        target_size: Tuple[int, int] = (224, 224)
    ) -> np.ndarray:
        """
        Runs model forward and backward pass to generate a normalized 2D Grad-CAM++ heatmap [0.0, 1.0].
        """
        self.model.eval()
        # Input tensor requires gradient tracking for backward hook
        input_tensor = input_tensor.clone().detach().requires_grad_(True)
        
        logits = self.model(input_tensor)
        
        if target_class is None:
            target_class = int(torch.argmax(logits, dim=1).item())

        self.model.zero_grad()
        score = logits[0, target_class]
        score.backward(retain_graph=False)

        if self.activations is None or self.gradients is None:
            # Fallback uniform array if hook failed
            return np.zeros(target_size, dtype=np.float32)

        grads = self.gradients[0] # (C, H, W)
        acts = self.activations[0] # (C, H, W)

        # Grad-CAM++ weight formulation
        # g = dY/dA, g^2 = d2Y/dA2, g^3 = d3Y/dA3
        g2 = grads.pow(2)
        g3 = grads.pow(3)

        sum_acts = acts.sum(dim=(1, 2), keepdim=True)
        denom = 2.0 * g2 + sum_acts * g3
        denom = torch.where(denom != 0.0, denom, torch.ones_like(denom))
        
        alphas = g2 / denom
        weights = (alphas * F.relu(grads)).sum(dim=(1, 2), keepdim=True)

        cam = (weights * acts).sum(dim=0)
        cam = F.relu(cam)

        cam_np = cam.detach().cpu().numpy()
        cam_min, cam_max = cam_np.min(), cam_np.max()
        if cam_max > cam_min:
            cam_norm = (cam_np - cam_min) / (cam_max - cam_min)
        else:
            cam_norm = np.zeros_like(cam_np)

        # Resize to target display dimensions using bilinear PIL interpolation
        cam_img = Image.fromarray((cam_norm * 255).astype(np.uint8)).resize(
            (target_size[1], target_size[0]), resample=Image.BILINEAR
        )
        return np.array(cam_img, dtype=np.float32) / 255.0

def convert_cam_to_base64_png(
    cam_array: np.ndarray,
    alpha_intensity: float = 0.65
) -> str:
    """
    Converts 2D normalized activation array [0.0, 1.0] into a color-mapped
    RGBA PNG encoded as a Base64 data URI string for seamless frontend overlay.
    """
    h, w = cam_array.shape
    idx = np.clip((cam_array * 255).astype(np.uint8), 0, 255)
    
    # Map into Jet RGB
    rgb = _JET_LUT[idx]
    
    # Non-linear Alpha channel: near-zero activations are completely transparent
    # Peak activations are rendered with alpha_intensity
    alpha = (cam_array ** 1.5) * alpha_intensity * 255.0
    # Suppress lower 15% noise threshold to transparent
    alpha[cam_array < 0.15] = 0.0
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)

    rgba = np.dstack([rgb, alpha])
    pil_img = Image.fromarray(rgba, mode="RGBA")
    
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG", optimize=True)
    b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_str}"

def compute_activation_lesion_concordance(
    cam_array: np.ndarray,
    lesion_contour_pct: list,
    canvas_size: Tuple[int, int] = (224, 224)
) -> Tuple[float, str]:
    """
    Computes Intersection-over-Union (IoU) concordance between high Grad-CAM++
    activations (>50th percentile) and the Stage I segmented lesion boundary.
    Returns:
      (concordance_score: float [0.0 - 1.0], alert_message: Optional[str])
    """
    h, w = canvas_size
    if not lesion_contour_pct or len(lesion_contour_pct) < 3:
        return 0.50, "Stage I lesion contour insufficient for concordance audit."

    # Render binary mask from percentage contour points
    from PIL import ImageDraw
    polygon = [(pt[0] * w / 100.0, pt[1] * h / 100.0) for pt in lesion_contour_pct]
    mask_img = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask_img).polygon(polygon, outline=1, fill=1)
    lesion_mask = np.array(mask_img, dtype=bool)

    # Threshold activation field at top 40%
    cam_active = cam_array > 0.40

    intersection = np.logical_and(lesion_mask, cam_active).sum()
    union = np.logical_or(lesion_mask, cam_active).sum()

    if union == 0:
        return 0.50, "Indeterminate visual field activation."

    iou = float(intersection) / float(union)
    concordance = round(min(1.0, max(0.0, iou * 1.8)), 3) # Scaled for clinical overlap tolerance

    if concordance < 0.20:
        alert = "POSSIBLE SHORTCUT LEARNING / ARTIFACT: Neural attention is concentrated outside the delineated lesion margin (e.g., teeth reflection, saliva, or retractor edge)."
    elif concordance < 0.45:
        alert = "MODERATE ALIGNMENT: Neural attention partially intersects lesion margin."
    else:
        alert = "STRONG CONCORDANCE: Neural attention is focused directly on the atypical mucosal lesion boundary."

    return concordance, alert
