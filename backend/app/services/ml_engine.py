import gc
import logging
from typing import Tuple
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
from torchvision.models.vgg import make_layers, cfgs

from app.core.config import settings
from app.services.image_quality import compute_image_quality

logger = logging.getLogger(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class MergedNet(nn.Module):
    def __init__(self, num_classes: int = 2):
        super(MergedNet, self).__init__()
        # Direct feature construction saves >450 MB by skipping VGG16's unused classifier
        self.vgg_features = make_layers(cfgs["D"])
        self.vgg_pool = nn.AdaptiveAvgPool2d((7, 7))

        res = models.resnet50(weights=None)
        self.res_features = nn.Sequential(*list(res.children())[:-2])

        eff = models.efficientnet_b0(weights=None)
        self.eff_features = eff.features

        mob = models.mobilenet_v2(weights=None)
        self.mob_features = mob.features

        self.pool = nn.AdaptiveAvgPool2d((1, 1))

        # Total feature dimension: 512 + 2048 + 1280 + 1280 = 5120
        self.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(5120, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x_vgg = self.pool(self.vgg_pool(self.vgg_features(x))).view(x.size(0), -1)
        x_res = self.pool(self.res_features(x)).view(x.size(0), -1)
        x_eff = self.pool(self.eff_features(x)).view(x.size(0), -1)
        x_mob = self.pool(self.mob_features(x)).view(x.size(0), -1)
        out = torch.cat((x_vgg, x_res, x_eff, x_mob), dim=1)
        return self.fc(out)

# Transforms
inference_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

tta_transforms = [
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomHorizontalFlip(p=1.0), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomVerticalFlip(p=1.0), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomRotation(degrees=(15, 15)), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomRotation(degrees=(-15, -15)), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.ColorJitter(brightness=0.2), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.ColorJitter(contrast=0.2), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomGrayscale(p=0.5), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    inference_transform,
]

class_names = ["cancer", "non_cancer"]

# Singleton Model Loader
_ai_model = None

def get_model() -> MergedNet:
    global _ai_model
    if _ai_model is not None:
        return _ai_model
        
    logger.info(f"Initializing AI Model on {device}...")
    model = MergedNet(num_classes=2)
    
    if not settings.MODEL_PATH.exists():
        logger.warning(f"Model checkpoint not found at: {settings.MODEL_PATH}. Starting with random weights.")
        model.eval()
        model.to(device)
        _ai_model = model
        return _ai_model
        
    state_dict = torch.load(settings.MODEL_PATH, map_location=device)
    with torch.no_grad():
        for name, param in model.named_parameters():
            if name in state_dict:
                param.copy_(state_dict[name].float())
        for name, buf in model.named_buffers():
            if name in state_dict:
                buf.copy_(state_dict[name].float())
                
    del state_dict
    gc.collect()
    model.eval()
    model.to(device)
    logger.info("AI Model successfully initialized in low-memory mode.")
    _ai_model = model
    return _ai_model

def run_inference_pipeline(image: Image.Image) -> Tuple[str, float, float, float]:
    """
    Executes full clinical deep learning pipeline:
      1. Image quality analysis (sharpness via Laplacian variance)
      2. Test-Time Augmentation (8 passes)
      3. Monte Carlo Dropout (15 stochastic forward passes)
      4. Epistemic uncertainty computation
    """
    model = get_model()
    img_array = np.array(image)
    quality_score = compute_image_quality(img_array)

    # 1. TTA passes
    tta_probs = []
    with torch.no_grad():
        for t in tta_transforms:
            tensor = t(image).unsqueeze(0).to(device)
            out = model(tensor)
            tta_probs.append(torch.nn.functional.softmax(out, dim=1))
    tta_mean = torch.stack(tta_probs).mean(dim=0)

    # 2. Monte Carlo Dropout passes
    model.train()  # Enable stochastic dropout
    mcd_preds = []
    with torch.no_grad():
        base_tensor = inference_transform(image).unsqueeze(0).to(device)
        for _ in range(settings.MC_DROPOUT_PASSES):
            out = model(base_tensor)
            mcd_preds.append(torch.nn.functional.softmax(out, dim=1))
    model.eval()   # Restore evaluation mode

    mcd_stack = torch.stack(mcd_preds)
    mcd_mean = mcd_stack.mean(dim=0)
    mcd_var = mcd_stack.var(dim=0)

    # 3. Fuse TTA and MCD probabilities
    final_probs = 0.5 * tta_mean + 0.5 * mcd_mean
    confidence, pred_idx = torch.max(final_probs, 1)
    
    pred_class = class_names[pred_idx.item()]
    confidence_score = float(confidence.item())
    uncertainty = float(mcd_var.max().item())

    # Uncertainty gating
    if uncertainty > settings.UNCERTAINTY_THRESHOLD:
        pred_class = "uncertain"

    return pred_class, confidence_score, uncertainty, quality_score
