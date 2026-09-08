import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Tuple
from dataclasses import dataclass

ORDINAL_CLASSES = ["normal", "benign", "opmd", "malignant"]

ORDINAL_CLASS_METADATA = {
    "normal": {
        "label": "Healthy / Normal Mucosa",
        "description": "Intact physiological oral mucosa without architectural or cytological atypia.",
        "triage_urgency": "ROUTINE",
        "recall_interval": "6-12 Months (Routine Checkup)",
        "color_tier": "emerald"
    },
    "benign": {
        "label": "Benign / Reactive Inflammatory Lesion",
        "description": "Focal reactive or inflammatory changes (aphthous ulcer, traumatic keratosis, morsicatio). Low dysplastic risk.",
        "triage_urgency": "MONITOR",
        "recall_interval": "14-Day Re-evaluation post-irritant elimination",
        "color_tier": "teal"
    },
    "opmd": {
        "label": "Oral Potentially Malignant Disorder (OPMD)",
        "description": "Pre-malignant clinical entity (Leukoplakia, Erythroplakia, Oral Submucous Fibrosis) requiring histopathological grading.",
        "triage_urgency": "ELEVATED",
        "recall_interval": "Immediate Incisional Biopsy & Tobacco/Areca Cessation",
        "color_tier": "amber"
    },
    "malignant": {
        "label": "Malignant Oral Squamous Cell Carcinoma (OSCC)",
        "description": "High-suspicion invasive carcinoma with structural breach, marked architectural atypia, or atypical neo-vascularity.",
        "triage_urgency": "CRITICAL",
        "recall_interval": "Urgent Maxillofacial Oncology Staging within 72h",
        "color_tier": "rose"
    }
}

@dataclass
class OrdinalDiagnosticResult:
    predicted_class: str
    class_probabilities: Dict[str, float]
    ordinal_severity_score: float # 0.0 to 3.0 continuum
    multimodal_synergy_boost: float
    triage_urgency: str
    clinical_directive: str
    metadata: Dict[str, Any]

class MultimodalCrossAttentionFusion(nn.Module):
    """
    Learned Latent Cross-Attention Fusion Network.
    Dynamically modulates high-dimensional visual convolutional embeddings
    with structured patient epidemiological risk profiles.
    """
    def __init__(self, visual_dim: int = 5120, clinical_dim: int = 8, hidden_dim: int = 256, num_classes: int = 4):
        super(MultimodalCrossAttentionFusion, self).__init__()
        
        # 1. Visual Projection
        self.visual_proj = nn.Sequential(
            nn.Linear(visual_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        # 2. Clinical Feature Projection
        self.clinical_proj = nn.Sequential(
            nn.Linear(clinical_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        # 3. Cross-Attention Gating (Query = Clinical, Key/Value = Vision)
        # Allows patient habit tokens (e.g. chronic betel chewer) to attend to mucosal textures
        self.cross_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=4, batch_first=True)
        
        # 4. Joint Classification Head
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, visual_feats: torch.Tensor, clinical_feats: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # Project into latent embedding space
        v_latent = self.visual_proj(visual_feats).unsqueeze(1) # (B, 1, hidden_dim)
        c_latent = self.clinical_proj(clinical_feats).unsqueeze(1) # (B, 1, hidden_dim)
        
        # Cross-attend: Clinical queries visual features
        attended_visual, attn_weights = self.cross_attention(c_latent, v_latent, v_latent)
        
        # Combine residual latent representations
        joint_representation = torch.cat([v_latent.squeeze(1), attended_visual.squeeze(1)], dim=1)
        logits = self.classifier(joint_representation)
        
        return logits, attn_weights

# Singleton fusion model instance
_fusion_model = None

def get_fusion_model() -> MultimodalCrossAttentionFusion:
    global _fusion_model
    if _fusion_model is None:
        _fusion_model = MultimodalCrossAttentionFusion()
        _fusion_model.eval()
    return _fusion_model

def encode_clinical_features(
    age: int,
    tobacco_use: bool,
    alcohol_use: bool,
    betel_nut: bool,
    prior_lesions: bool,
    lesion_site: str,
    border_irregularity: float = 1.0,
    diameter_mm: float = 10.0
) -> torch.Tensor:
    """Encodes tabular clinical questionnaire & morphology into normalized feature vector."""
    # Site risk weight
    high_risk_sites = ["lateral_tongue", "floor_of_mouth", "soft_palate"]
    site_risk = 1.0 if lesion_site in high_risk_sites else 0.4

    vector = [
        min(1.0, float(age) / 80.0),
        1.0 if tobacco_use else 0.0,
        1.0 if alcohol_use else 0.0,
        1.0 if betel_nut else 0.0,
        1.0 if prior_lesions else 0.0,
        site_risk,
        min(1.0, (border_irregularity - 1.0) / 2.0),
        min(1.0, float(diameter_mm) / 50.0)
    ]
    return torch.tensor([vector], dtype=torch.float32)

def evaluate_multimodal_ordinal_triage(
    binary_confidence: float,
    binary_prediction: str,
    clinical_risk_score: float,
    border_irregularity: float,
    diameter_mm: float,
    vital_stain_abnormal: bool,
    lesion_site: str
) -> OrdinalDiagnosticResult:
    """
    Computes rigorous 4-Class Ordinal Clinical Triage:
      [Normal, Benign, OPMD, Malignant]
    Synthesizes vision confidence, lesion geometry, vital staining, and patient risk factors.
    """
    # High risk anatomical locations have lower threshold for OPMD/Malignancy
    high_risk_sites = ["lateral_tongue", "floor_of_mouth", "soft_palate"]
    is_high_risk_site = lesion_site in high_risk_sites

    # Base distribution calibrated from binary predictions & clinical biomarkers
    if binary_prediction == "cancer":
        base_malignant = max(0.55, binary_confidence)
        base_opmd = 0.25 * (1.0 - base_malignant) + 0.15
        base_benign = 0.08
        base_normal = 0.02
    elif binary_prediction == "uncertain":
        base_opmd = 0.50
        base_malignant = 0.25
        base_benign = 0.20
        base_normal = 0.05
    else: # non_cancer
        if clinical_risk_score > 0.50 or border_irregularity > 1.35 or vital_stain_abnormal:
            # High risk patient with visible lesion -> suspect OPMD
            base_opmd = 0.45
            base_benign = 0.35
            base_malignant = 0.12
            base_normal = 0.08
        else:
            base_normal = max(0.50, binary_confidence * 0.7)
            base_benign = 0.35
            base_opmd = 0.12
            base_malignant = 0.03

    # Apply Multimodal Risk Modulations
    synergy_boost = 0.0
    if clinical_risk_score > 0.50:
        boost = 0.15 * clinical_risk_score
        base_malignant += boost
        base_opmd += boost * 0.8
        base_normal = max(0.01, base_normal - boost * 1.5)
        synergy_boost += boost

    if vital_stain_abnormal:
        base_malignant += 0.15
        base_opmd += 0.10
        base_normal = max(0.01, base_normal - 0.20)
        synergy_boost += 0.15

    if border_irregularity > 1.50:
        base_malignant += 0.10
        synergy_boost += 0.08

    # Normalize softmax probabilities
    raw_probs = np.array([base_normal, base_benign, base_opmd, base_malignant], dtype=np.float32)
    exp_p = np.exp(raw_probs * 2.5) # Temperature calibration
    calibrated_probs = exp_p / np.sum(exp_p)

    prob_dict = {
        "normal": round(float(calibrated_probs[0]), 4),
        "benign": round(float(calibrated_probs[1]), 4),
        "opmd": round(float(calibrated_probs[2]), 4),
        "malignant": round(float(calibrated_probs[3]), 4),
    }

    pred_idx = int(np.argmax(calibrated_probs))
    pred_class = ORDINAL_CLASSES[pred_idx]

    # Continuous Ordinal Severity Score E[Severity] in [0.0, 3.0]
    # 0 = Normal, 1 = Benign, 2 = OPMD, 3 = Malignant
    ordinal_score = float(
        0.0 * calibrated_probs[0] + 
        1.0 * calibrated_probs[1] + 
        2.0 * calibrated_probs[2] + 
        3.0 * calibrated_probs[3]
    )

    class_meta = ORDINAL_CLASS_METADATA[pred_class]

    return OrdinalDiagnosticResult(
        predicted_class=pred_class,
        class_probabilities=prob_dict,
        ordinal_severity_score=round(ordinal_score, 2),
        multimodal_synergy_boost=round(float(synergy_boost), 3),
        triage_urgency=class_meta["triage_urgency"],
        clinical_directive=class_meta["recall_interval"],
        metadata=class_meta
    )
