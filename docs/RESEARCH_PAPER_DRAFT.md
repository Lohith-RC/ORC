# Oral Cancer Detection Using AI/ML and Deep Learning

**Authors:** Rakshith Y B, Lohith R C, Keerthi A  
*(Author order provisional, subject to project guide confirmation)*  
**Institutional Affiliation:** Department of Computer Science & Engineering, Kalpataru Institute of Technology, Tiptur, Karnataka, India  
*(Affiliated with Visvesvaraya Technological University, Belagavi)*  
**Project Guide:** Aishwarya S *(Project Guide, Department of Computer Science & Engineering, Kalpataru Institute of Technology; guide role only, omitted from author byline)*  
**Academic Context:** Final-Year B.E. Computer Science and Engineering Capstone Project  
**Date:** October 2026  

---

## 1. Abstract

**Abstract—**This paper describes the software design and implementation of a non-diagnostic prototype for binary oral image classification. Its PyTorch MergedNet model combines pooled visual features from VGG-16, ResNet-50, EfficientNet-B0, and MobileNetV2 into a 5,120-dimensional representation. The application includes a React frontend and a FastAPI backend; its inference code also contains test-time augmentation and Monte Carlo dropout uncertainty logic, with differences between the PyTorch and ONNX execution paths. The inspected repository contains 940 JPEG images arranged in cancer and non-cancer classes. A hash audit found 21 groups of exact duplicates encompassing 46 individual files (25 redundant copies), including 11 groups (25 files, 14 redundant copies) that cross data partitions. Patient identifiers are unavailable, and the dataset’s original provenance and usage terms have not been verified. Although a model checkpoint is present, reproducible training records and empirical evaluation on the dataset were not found. Previously reported benchmark figures, including 99.92% accuracy, were generated synthetically and are not model test results. Accordingly, this paper makes no classification-performance or clinical-effectiveness claims. No evidence of regulatory clearance was found in the inspected repository, regulatory status has not been assessed, and the prototype is not clinically validated and is not intended for clinical use. It documents the prototype’s implementation and its data, evaluation, and validation limitations.

---

## 2. Keywords

oral image classification; deep learning; feature fusion; uncertainty estimation; decision-support prototype

---

## 3. Introduction

Oral cancer represents a notable global public health challenge. According to GLOBOCAN 2020 statistics, cancers of the lip and oral cavity accounted for an estimated 377,713 new cases and 177,757 deaths worldwide in 2020 [1]. Frontline screening strategies evaluated in a Cochrane systematic review center on conventional visual and tactile oral mucosal examinations; while evidence from a randomized trial suggested a reduction in oral cancer mortality in targeted high-risk individuals (tobacco or alcohol users), the review concluded that evidence to support screening programmes across the general population remains insufficient [2].

To explore software tools that could support frontline image review, automated photographic analysis using computer vision and deep learning has become an active area of medical-image analysis research [3], [4]. In this paper, the term "decision-support prototype" is defined specifically as terminology used in this paper to designate an exploratory software application intended to assist users in organizing, viewing, and reviewing photographic images, rather than as a universal clinical definition; the prototype is fundamentally **not** an autonomous diagnostic medical device. The prototype documented in this paper is strictly non-diagnostic: repository specifications and system requirements explicitly state that the software is not a substitute for biopsy, histopathology, or formal clinical evaluation by qualified healthcare specialists.

A central engineering design choice in visual image classification involves selecting an appropriate convolutional neural network (CNN) architecture. Individual convolutional backbones possess different architectural properties, receptive fields, and feature-extraction behaviors. For example, deep architectures with homogenous stacks of $3\times3$ convolutions (such as VGG-16) extract deep spatial feature hierarchies through increasing channel capacity across sequential pooling stages [5], residual networks (such as ResNet-50) incorporate residual connections that support the optimization and training of deeper network representations [6], and compact architectures (such as MobileNetV2 and EfficientNet-B0) optimize computational efficiency using depthwise separable convolutions with inverted residuals [7] and compound scaling across depth, width, and resolution [8]. Combining representations extracted across multiple diverse backbones—a technique known as *feature fusion*—aims to supply downstream classification layers with a composite feature vector containing representations from multiple topologies.

However, evaluating such prototypes from an engineering perspective requires addressing practical implementation and methodological realities:
1. **Model Uncertainty Quantification:** Deterministic neural networks output point predictions without representing parameter uncertainty. Incorporating uncertainty estimation mechanisms, such as Monte Carlo Dropout [9], provides a principled approximation of epistemic uncertainty during inference.
2. **Input Quality Checking:** The implemented application includes a heuristic image-quality and blur-detection check based on OpenCV Laplacian variance; however, the practical effect of this filtering mechanism on classification stability or user workflow has not been empirically evaluated in this project.
3. **Transparent Academic Reporting:** Scientific rigor requires clear differentiation between verified software implementations, empirical performance measurements on a properly separated test set, and synthetic or heuristic software routines. In this repository, the current test partition is affected by exact duplicates and cannot be treated as an independent test set.

### Objectives of This Paper
This paper presents an evidence-based system description of the oral image classification prototype based on a factual audit of the current repository. The specific objectives are:
1. To detail the system architecture of **MergedNet**, a multi-backbone feature fusion model implemented in PyTorch that fuses feature vectors from VGG-16 [5], ResNet-50 [6], EfficientNet-B0 [8], and MobileNetV2 [7].
2. To document the web application stack linking a React frontend client to an asynchronous FastAPI backend service.
3. To describe the inference-time uncertainty estimation routines present in code (Test-Time Augmentation and Monte Carlo Dropout) and detail the operational differences between the PyTorch and ONNX execution paths.
4. To disclose repository data limitations, including unverified dataset provenance, the presence of 21 duplicate image groups encompassing 46 files (with 11 groups encompassing 25 files crossing split boundaries), the absence of patient-level identifiers, missing reproducible training scripts, and the presence of synthetic benchmark generation scripts.
5. To articulate a conditional research roadmap outlining the technical and methodological prerequisites required before valid empirical performance claims can be evaluated.

---

## 4. Related Work

Developing decision-support prototypes for oral mucosal image analysis draws upon research across computer vision, machine learning, and medical informatics. This section summarizes related literature concepts across four focused domains.

### 4.1 Prior Deep Learning Studies in Oral Image Classification
Convolutional neural networks have been investigated across several dedicated photographic oral lesion datasets. In an exploratory study, Welikala et al. [3] evaluated deep learning architectures, including ResNet-50, on their own curated dataset of intraoral photographs to classify lesions into suspicious and non-suspicious categories. In a separate institutional investigation, Warin et al. [4] trained and evaluated deep CNN architectures on their own dataset of 980 photographic images (comprising 365 OSCC, 315 OPMD, and 300 non-pathological images), reporting classification metrics specific to their dataset and experimental setup.

While these studies demonstrate the algorithmic feasibility of training CNNs on specific image collections, they represent evaluations conducted strictly on their own distinct cohorts, and findings from prior research cohorts cannot be generalized to the unverified repository dataset or prototype evaluated in this project.

### 4.2 Feature Fusion Architecture
In this project, feature fusion refers specifically to the intermediate layer concatenation implemented in the MergedNet model. Global average pooled feature vectors extracted simultaneously from four distinct convolutional backbones—VGG-16 [5], ResNet-50 [6], EfficientNet-B0 [8], and MobileNetV2 [7]—are concatenated into a unified 5,120-dimensional representation that is fed directly into a common fully connected classification head.

### 4.3 Uncertainty Estimation in Deep Learning Systems
Standard deterministic deep neural networks output point estimates that do not represent prediction uncertainty [9]. In computational uncertainty literature, predictive uncertainty is broadly distinguished into two forms [9], [10]:
- **Epistemic (Model) Uncertainty:** Represents uncertainty in the network parameters arising from limited training data, which can theoretically be reduced with additional training samples. Gal and Ghahramani [9] formulated Monte Carlo Dropout (MCD) as a practical variational Bayesian approximation of deep Gaussian processes. By keeping dropout active at test time across repeated stochastic forward passes, the variance across the resulting predictive distribution provides a tractable estimate of epistemic model uncertainty [9].
- **Aleatoric (Data) Uncertainty:** Represents input-dependent uncertainty inherent to the observation process (such as image noise, optical artifacts, or blur), which cannot be eliminated simply by collecting more training data. Ayhan and Berens [10] investigated Test-Time Augmentation (TTA) in medical imaging, demonstrating that evaluating prediction dispersion across label-preserving geometric and optical perturbations can provide an empirical measure of data-dependent (aleatoric) uncertainty.

Importantly, while the prototype studied in this paper incorporates code for both Monte Carlo dropout and test-time augmentation in its inference pipeline, TTA is implemented in the codebase as an unweighted probability-averaging heuristic alongside an ad-hoc variance check. Neither method has been empirically calibrated or clinically validated as an uncertainty estimator on the repository's dataset [TO VERIFY].

### 4.4 Dataset Integrity, Partition Leakage, and Methodological Rigor
Systematic reviews and methodological surveys of machine learning literature have documented widespread vulnerabilities that undermine reported findings in published studies [11], [12]:
- **Data Contamination via Duplicate Images:** The repository audit identified exact duplicates across partitions. Exact duplicates could contaminate evaluation if the supplied training split was used to train the checkpoint [11], [12]. However, because the training history is missing, it cannot be confirmed whether the model actually saw those test images during training. In a literature survey across 17 quantitative fields, Kapoor and Narayanan [12] introduced an eight-part taxonomy of data leakage types, demonstrating that data leakage frequently produces overoptimistic performance conclusions.
- **Absence of Patient-Level Partitioning:** If multiple photographs collected from the same subject are divided randomly across training and testing sets, models can memorize patient-specific confounding features (such as surrounding dentition, skin pigmentation, or camera characteristics) rather than pathological indicators [11]. In their review of machine learning pitfalls in COVID-19 imaging, Roberts et al. [11] identified the failure to isolate patient records into disjoint splits as a primary source of bias and inflated reported accuracy.
- **Missing Dataset Documentation in the Repository:** In this repository, documentation regarding data provenance, original clinical sources, ethical approvals, and licensing terms is absent [TO VERIFY]. In their study of COVID-19 imaging pitfalls, Roberts et al. [11] highlighted that missing source documentation and unclear dataset lineage impede scientific validation.

---

## 5. System and Methods

This section documents the verified software architecture, repository dataset status, feature fusion model structure, and uncertainty estimation mechanisms implemented in the prototype.

```
+--------------------------------------------------------------------------------+
|                             REACT WEB FRONTEND                                 |
|  - Photographic Image Upload (.jpg, .png, .webp)                               |
|  - Client-Side Blur Check (Canvas Laplacian Variance Heuristic)                |
|  - Anatomical Site Selection & Context Questionnaire                           |
+--------------------------------------------------------------------------------+
                                       |
                                HTTP / REST API
                                       v
+--------------------------------------------------------------------------------+
|                            FASTAPI BACKEND SERVICE                             |
|  - MIME Validation & 64 KB Chunk Streaming (<= 10 MB limit)                    |
|  - Threaded Asynchronous Execution (anyio.to_thread.run_sync)                  |
|  - Image Sharpness Check (OpenCV Laplacian Variance, Threshold = 50.0)         |
+--------------------------------------------------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|                        MERGEDNET FEATURE FUSION ENGINE                         |
|                                                                                |
|   Input Image (3 x 224 x 224, ImageNet Normalized)                             |
|        |                                                                       |
|   +----+--------------------+--------------------+--------------------+        |
|   |                         |                    |                    |        |
|   v                         v                    v                    v        |
| [VGG-16]               [ResNet-50]        [EfficientNet-B0]    [MobileNetV2]   |
| Config 'D' Feat. [5]   Bottleneck Feat. [6] Conv Features [8]  Inverted Res. [7]|
| AdaptPool2d(7x7)            |                    |                    |        |
| AdaptPool2d(1x1)       AdaptPool2d(1x1)   AdaptPool2d(1x1)     AdaptPool2d(1x1)|
|   | (512-d)                 | (2048-d)           | (1280-d)           | (1280-d|
|   +----+--------------------+--------------------+--------------------+        |
|        |                                                                       |
|        v                                                                       |
| Concatenated Feature Vector: 5,120 Total Dimensions                            |
|        |                                                                       |
|        v                                                                       |
| Fully Connected Classification Head:                                           |
|   - Dropout (p = 0.5)                                                          |
|   - Linear Layer (5,120 -> 512) -> ReLU                                        |
|   - Dropout (p = 0.3)                                                          |
|   - Linear Output Layer (512 -> 2 classes: 'cancer', 'non_cancer')             |
+--------------------------------------------------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|                   UNCERTAINTY GATING & INFERENCE PIPELINE                      |
|  - PyTorch Path: 8 TTA Transforms [10] + 15 MC Dropout Passes [9] (Avg. Probs) |
|  - ONNX Path: 2 TTA Transforms + Base Image (3 Passes, TTA Variance Only)      |
|  - Threshold Gating: Variance > 0.015 flags output as "uncertain"              |
+--------------------------------------------------------------------------------+
```

### 5.1 System Architecture Overview
The application uses a decoupled client-server structure:
- **Frontend Presentation Layer:** Built with React.js, providing an interface for uploading oral images, executing client-side image blur checks, selecting anatomical locations, and viewing model output flags.
- **Backend Service Layer:** Implemented in Python using the FastAPI framework, handling REST API requests, file ingestion boundaries, image preprocessing, and inference orchestration.
- **Inference Execution Engine:** Executes model forward passes via PyTorch, with an alternative execution path using ONNX Runtime for CPU environments.

### 5.2 Dataset Characteristics and Inspection Findings
Inspection of the repository filesystem confirms an image collection arranged into folder partitions. Table 1 lists the verified image counts:

**Table 1: Repository Image Counts by Partition**
| Partition | Cancer Class | Non-Cancer Class | Partition Total |
| :--- | :---: | :---: | :---: |
| **Train** | 341 | 314 | 655 |
| **Validation** | 75 | 68 | 143 |
| **Test** | 74 | 68 | 142 |
| **Total** | **490** | **450** | **940** |

All images are stored in JPEG format. Preprocessing transforms resize incoming images to 224 × 224 pixels. A factual audit reveals several critical data constraints:
1. **Unverified Source and Provenance:** Project documents describe the dataset as originating from Kaggle. However, the exact Kaggle URL, original uploader, source clinic or hospital, image collection device specifications, and copyright/usage licenses were not identified in the repository and remain unverified [TO VERIFY]. The images cannot be described as verified public, clinical, hospital-collected, or multi-center data.
2. **Absence of Patient-Level Identifiers:** The repository files lack patient identification numbers, clinical case records, or subject-level metadata. It is therefore impossible to determine how many unique subjects contributed to the 940 images, creating a potential risk of patient overlap across partitions.
3. **Duplicate Images and Cross-Partition Leakage:** A cryptographic SHA-256 hash audit identified **21 exact duplicate groups** encompassing **46 individual image files** (representing **25 redundant copies** across 21 unique images), of which **11 groups (encompassing 25 files, representing 14 redundant copies) cross data partitions** (appearing in multiple split folders, including train and test). Because identical files exist simultaneously in training and test partitions, the existing test partition cannot be described as a properly separated, independent, or statistically valid test set.
4. **Absence of Governance Documentation:** No documentation of Institutional Review Board (IRB) ethics approval, patient informed consent, or formal data licensing was found in the inspected repository [TO VERIFY]. This does not establish that approvals do not exist externally, but confirms that no supporting governance documentation is present in the codebase.

### 5.3 The MergedNet Feature Fusion Architecture
The primary neural network defined in `app/services/ml_engine.py` is **MergedNet**, a PyTorch `nn.Module` configured for binary classification (*cancer* vs. *non-cancer*). Rather than relying on a single backbone, MergedNet extracts features simultaneously from four convolutional architectures:

1. **VGG-16 Backbone:** Uses convolutional feature layers from VGG-16 configuration "D" [5] (13 convolutional layers across five blocks). The original fully connected classifier is omitted. Feature maps are processed through an adaptive average pooling layer of size (7, 7) followed by global adaptive average pooling of size (1, 1), producing a **512-dimensional** vector.
2. **ResNet-50 Backbone:** Uses the residual bottleneck convolutional feature extractor [6], extracted by taking child layers excluding the final pooling and linear layers (`list(res.children())[:-2]`). Global adaptive average pooling (1, 1) compresses this output into a **2,048-dimensional** vector.
3. **EfficientNet-B0 Backbone:** Incorporates the mobile inverted bottleneck convolutional blocks [8] (`eff.features`), compressed via global adaptive average pooling (1, 1) to produce a **1,280-dimensional** vector.
4. **MobileNetV2 Backbone:** Employs the inverted residual convolutional structure [7] (`mob.features`), processed through global adaptive average pooling (1, 1) to produce a **1,280-dimensional** vector.

#### Feature Concatenation and Classifier Head
The four pooled feature vectors are flattened and concatenated along the channel dimension into a unified representation $\mathbf{z}$:

$$\text{dim}(\mathbf{z}) = 512 + 2048 + 1280 + 1280 = 5,120$$

This 5,120-dimensional concatenated vector is passed into a fully connected classification head consisting of:
- **Dropout Layer 1:** Dropout probability $p = 0.5$.
- **Linear Hidden Layer:** Linear transformation from 5,120 dimensions to 512 units.
- **Activation Function:** Rectified Linear Unit ($\text{ReLU}$).
- **Dropout Layer 2:** Dropout probability $p = 0.3$.
- **Linear Output Layer:** Final linear transformation from 512 units to 2 output logits corresponding to the two classes.

*Note on Pre-Training Status:* While standard implementations of these architectures frequently use ImageNet pre-trained weights, the repository code instantiates backbones with `weights=None` before copying parameters from the checkpoint file `merged_model.pth`. The original initialization and pre-training history are not documented in the repository [TO VERIFY].

### 5.4 Uncertainty Estimation and Inference Pipelines
The backend codebase contains uncertainty estimation logic intended to detect ambiguous predictions. Code inspection reveals two distinct implementation paths:

#### Path A: Native PyTorch Pipeline (TTA + Monte Carlo Dropout)
When executing via PyTorch, the inference pipeline in `run_inference_pipeline` implements:
1. **Test-Time Augmentation (TTA):** Evaluates eight image variants (horizontal flip, vertical flip, $+15^\circ$ rotation, $-15^\circ$ rotation, brightness jitter, contrast jitter, random grayscale, and standard resize/normalization) [10]. Softmax outputs from these eight passes are averaged to compute a mean probability vector $\bar{P}_{\text{TTA}}$.
2. **Monte Carlo Dropout (MCD):** The function `_enable_dropout_only` sets dropout modules to training mode (`m.train()`) while keeping batch normalization layers in evaluation mode, following the Monte Carlo Dropout paradigm [9]. An input tensor is repeated across multiple stochastic passes ($N_{\text{passes}} = 15$), and the mean $\bar{P}_{\text{MCD}}$ and variance $\sigma^2_{\text{MCD}}$ across passes are computed.
3. **Ensemble Combination and Threshold Gating:** The code combines probabilities as an unweighted average:

$$P_{\text{final}} = 0.5 \cdot \bar{P}_{\text{TTA}} + 0.5 \cdot \bar{P}_{\text{MCD}}$$

The epistemic uncertainty value is assigned as the maximum variance across classes: $U = \max(\sigma^2_{\text{MCD}})$. If $U > \tau_{\text{uncertainty}}$ (configured to $\tau = 0.015$), the returned class is set to **"uncertain"**. In this path, TTA variance is not incorporated into the scalar uncertainty metric $U$.

#### Path B: ONNX Runtime Engine Path
The repository also provides an optimized ONNX Runtime execution path (`merged_model_int8.onnx` / `merged_model.onnx`):
- The ONNX path executes the base image plus two augmented transforms (horizontal flip and vertical flip), calculating variance across these three passes.
- Monte Carlo Dropout is **not executed** in the ONNX runtime path because exported ONNX graphs treat dropout operations as fixed identity layers in evaluation mode.
- Output variance is computed from the three TTA passes rather than stochastic dropout.

Importantly, while Ayhan and Berens [10] showed that TTA can estimate heteroscedastic aleatoric uncertainty in calibrated settings, the ad-hoc variance calculations in this prototype's PyTorch and ONNX routines have not been shown to reliably quantify aleatoric or epistemic uncertainty on oral images, and the exact end-to-end runtime stability and aggregation behavior during live multi-request execution remain [TO VERIFY].

---

## 6. Implementation

This section details the software implementation, distinguishing implemented neural network models from supporting rule-based and heuristic software modules.

### 6.1 Backend Web Service Implementation
The backend service is built using FastAPI and Python 3.10+:
- **Asynchronous Execution:** Model forward passes are dispatched via `anyio.to_thread.run_sync` to prevent blocking the asynchronous event loop during compute-intensive inference.
- **Payload Boundaries:** Uploaded files are read in 64 KB streaming chunks with an explicit 10 MB maximum file size limit. Permitted MIME types are restricted to `image/jpeg`, `image/png`, and `image/webp`.
- **Model Lifecycle Management:** Model weights are loaded once during application startup as a singleton instance protected by a `threading.Lock` to serialize inference passes.

### 6.2 Frontend Interface Implementation
The frontend is implemented as a React.js single-page application:
- **Client-Side Blur Screening:** A client-side JavaScript utility calculates image gradient variances on an HTML5 canvas to provide a preliminary blur warning before network transmission.
- **Anatomical Tagging:** An interactive SVG-based oral cavity map allows users to designate the anatomical region of the photographed lesion (e.g., buccal mucosa, lateral tongue, gingiva).
- **Status Flag Presentation:** The user interface displays categorical output badges, blur advisories, and uncertainty flags.

### 6.3 Differentiation of Machine Learning vs. Heuristic Components
To ensure accurate technical reporting, Table 2 categorizes all analytical modules present in the repository, differentiating neural network components from rule-based and heuristic algorithms:

**Table 2: Categorization of Repository Software Components**
| Functional Component | Code Location | Implemented Mechanism | Category |
| :--- | :--- | :--- | :--- |
| **Oral Image Classification** | `app/services/ml_engine.py` | PyTorch MergedNet (4-backbone feature fusion) [5]–[8] | **Neural Network** (Checkpoint Present) |
| **Image Sharpness Analysis** | `app/services/image_quality.py` | OpenCV Laplacian variance calculation (Threshold = 50.0) | **Deterministic Heuristic** (Non-ML) |
| **Specular Glare Suppression** | `app/services/optical_normalization.py` | Luminance thresholding + OpenCV inpainting | **Classical Computer Vision** (Non-ML) |
| **Color Normalization** | `app/services/optical_normalization.py` | Reinhard statistical mean/std transfer in LAB color space | **Statistical Color Mapping** (Non-ML) |
| **Lesion Boundary Segmentation** | `app/services/vision_pipeline.py` | Color heuristic: Erythema index `(R-G)/(R+G)` + brightness thresholding | **Handcrafted Heuristic** (Non-ML) |
| **Epidemiological Risk Scoring** | `app/services/clinical_risk.py` | Weighted linear sum: Age (+0.15–0.30), Tobacco (+0.35), Betel Nut (+0.30), Alcohol (+0.20) | **Rule-Based Formula** (Non-ML) |
| **Four-Class Ordinal Triage** | `app/services/multimodal_fusion.py` | Scripted modification of model probabilities using hardcoded bonus weights and temperature scaling (T=2.5) | **Rule-Based Formula** (Non-ML) |
| **AJCC Clinical Staging** | `app/services/clinical_staging.py` | Decision tree mapping lesion diameter and anatomical site to stage labels | **Rule-Based Logic** (Non-ML) |
| **Visual Interpretability (Grad-CAM++)** | `app/services/xai_cam.py` | Gradient-weighted Class Activation Mapping computed on ResNet-50 penultimate layer [13] | **Mathematical Post-Processing** |

*Note on Latent Cross-Attention Code:* The file `app/services/multimodal_fusion.py` contains a PyTorch class definition named `MultimodalCrossAttentionFusion`. However, live inspection confirms that this neural network module is not invoked during `/predict` request handling; instead, the live endpoint executes the rule-based function `evaluate_multimodal_ordinal_triage`.

### 6.4 Model Checkpoint Status and Missing Training History
The repository includes two compiled model files:
- `merged_model.pth` (PyTorch weight dictionary, ~94.7 MB)
- `merged_model_int8.onnx` (Quantized ONNX model, ~47.7 MB)

While these files load into the MergedNet model definition, **no training scripts, optimization configurations, or training logs are present in the repository** [TO VERIFY]. Essential training parameters—such as the optimizer (e.g., AdamW, SGD), learning rate, learning rate schedule, loss function formulation, batch size, epoch count, and data augmentation policies used during training—remain undocumented. Furthermore, training and validation loss curves are absent from the codebase.

---

## 7. Evaluation Status and Limitations

Transparent reporting requires full disclosure of how performance figures were generated and what evaluation data currently exists.

### 7.1 Disclosure of Synthetic Benchmark Generation Scripts
Internal project documents and prior drafts cited high classification figures, including an overall accuracy of **99.92%**, alongside comparative baseline tables and ablation studies.

Code inspection of the benchmark script (`backend/scripts/ieee_benchmark_evaluator.py`) reveals that **these reported figures are synthetic artifacts generated by random numerical simulation routines**. Specifically:
- The script implements a simulation function (`run_comparative_benchmark`) that generates synthetic sample sizes ($N = 1,200$) and draws prediction probabilities from parameterized statistical distributions (such as normal and beta random distributions).
- Performance metrics for baseline architectures (standalone ResNet-50, VGG-16, EfficientNet-B0, MobileNetV2) and ablation variants were generated by computing summary statistics over these synthetic random values.
- The script automatically exports these values into JSON records (`ieee_benchmark_results.json`) and formatted LaTeX tables (`ieee_tables.tex`).

These synthetic outputs represent an illustrative simulation script written during software development; **they do not represent empirical evaluations of the model on real images**. These figures are strictly excluded from this paper.

### 7.2 Absence of Reproducible Empirical Model Evaluation
Inspection of the repository found **no reproducible, verifiable empirical evaluation of the saved model weights (`merged_model.pth`) across the repository's image collection**.

Consequently:
- Real test-set performance metrics—including Classification Accuracy, Sensitivity, Specificity, Positive Predictive Value, Negative Predictive Value, F1-Score, and AUROC—are **currently unavailable** and marked [TO VERIFY].
- No claims of high classification accuracy, superior performance over baseline models, or diagnostic capability are made in this paper.

### 7.3 Data Integrity and Partition Leakage Limitations
The dataset presents several data integrity issues that preclude valid scientific conclusions:
1. **Duplicate Images Across Partitions:** The hash audit identified 21 exact duplicate image groups encompassing 46 files in total (representing 25 redundant copies), with **11 groups (encompassing 25 files, representing 14 redundant copies) crossing partition boundaries** (appearing in multiple split folders, including train and test). If the checkpoint was trained on the supplied training partition, evaluating it on this test partition could measure memorization rather than generalization [11], [12]; however, because training records are absent, actual sample exposure during training remains unverified.
2. **Lack of Patient-Level Separation:** In the absence of patient identifiers, it cannot be verified whether multiple photographs from the same individual exist across partitions. In biomedical machine learning literature, patient overlap between training and test sets has been documented as a frequent cause of performance overestimation [11], [12].
3. **Small Sample Size:** A total cohort of 940 images (490 cancer, 450 non-cancer) is modest for training a model architecture with 5,120 fused latent dimensions, introducing a significant risk of overfitting.

### 7.4 Ethical, Regulatory, and Clinical Boundaries
1. **No Ethics Documentation Found:** No documentation regarding Institutional Review Board (IRB) ethics approval, human subject protocols, or patient consent forms was found in the repository [TO VERIFY].
2. **Absence of Clinical Validation:** The prototype has not undergone prospective clinical trials, blinded reader studies with qualified clinicians, or validation on external cohorts.
3. **Non-Diagnostic and Regulatory Status:** The software does not possess medical device clearance or regulatory authorization (such as FDA, CE-IVD, or CDSCO approval). It is strictly a non-diagnostic software prototype and is not ready or approved for patient screening, triage, or clinical decision-making.

---

## 8. Discussion

### 8.1 Technical and Engineering Scope
The primary contribution of this work is the software engineering design and architectural implementation of a multi-backbone decision-support prototype. From a systems perspective:
- **Multi-Backbone Architecture:** MergedNet demonstrates an operational implementation for extracting and concatenating multi-scale visual features from four distinct CNN backbones [5]–[8] into a single classification head.
- **Uncertainty Quantification in Code:** The inclusion of Test-Time Augmentation [10] and Monte Carlo Dropout [9] illustrates how uncertainty estimation logic can be embedded into decision-support inference endpoints.
- **Decoupled Web Architecture:** The separation of a React client from an asynchronous, memory-bounded FastAPI backend demonstrates a practical architecture for serving deep learning models over HTTP.

### 8.2 Methodological Lessons
The audit of this undergraduate capstone project provides valuable methodological lessons for applied artificial intelligence research:
1. **The Necessity of Rigorous Data Auditing:** Performing cryptographic hash audits and verifying patient-level splits are essential first steps before conducting model training or evaluation [11], [12]. Data contamination across partitions invalidates reported test results.
2. **Transparent Documentation:** Distinguishing between mock simulation scripts (such as the synthetic benchmark evaluator) and genuine empirical evaluation on real data is vital for academic integrity.
3. **Clear Component Demarcation:** Auxiliary clinical tools—such as risk questionnaires and staging calculators—should be clearly documented as rule-based heuristics rather than conflated with trained machine learning models.

### 8.3 Conditional Remediation and Research Roadmap
Before valid empirical performance claims or further research exploration can be considered, the following conditional steps must be undertaken:

```
+--------------------------------------------------------------------------------+
|                 CONDITIONAL RESEARCH & REMEDIATION ROADMAP                     |
+--------------------------------------------------------------------------------+
                                       |
                                       v
[Phase 1: Dataset Provenance & Permissions (Conditional)]
  * Seek to identify the original source of the Kaggle dataset [TO VERIFY].
  * Confirm whether original ethical approvals, patient consent, and research-use
    permissions are documented and allow academic publication.
                                       |
                                       v
[Phase 2: Deduplication & Patient-Level Splitting (Conditional)]
  * Remove identical duplicate image files identified by SHA-256 hash matching.
  * If patient-level metadata can be obtained, ensure strict subject-level separation;
    otherwise, document the lack of patient-level isolation as a primary limitation.
  * Re-partition remaining unique images into mutually disjoint partitions.
                                       |
                                       v
[Phase 3: Reproducible Training Pipeline]
  * Write a version-controlled, reproducible PyTorch training script (`train.py`).
  * Explicitly specify loss formulation, optimizer, learning rate schedule, and seeds.
  * Record training loss, validation loss, and convergence logs transparently.
                                       |
                                       v
[Phase 4: Empirical Evaluation & Ablation Analysis]
  * Evaluate the retrained model on a properly separated, independent test set.
  * Calculate empirical metrics (Accuracy, Sensitivity, Specificity, F1, AUROC).
  * Conduct empirical ablation studies comparing MergedNet with individual backbones.
                                       |
                                       v
[Phase 5: Refinement of Auxiliary Modules (Conditional)]
  * Assess whether heuristic components (e.g., color-based segmentation) can be
    replaced with validated machine learning models (e.g., trained U-Net).
  * Re-evaluate rule-based risk scoring against established clinical literature.
                                       |
                                       v
[Phase 6: Clinical Collaboration (Conditional)]
  * In the event that Phases 1-5 are successfully completed and formal ethical
    clearance is established, collaborate with qualified clinical specialists to design
    prospective validation protocols.
```

---

## 9. Conclusion

This paper has documented the software design and implementation of a non-diagnostic prototype for binary oral image classification. The engineering framework implements **MergedNet**, a multi-backbone convolutional neural network combining pooled visual features from VGG-16 [5], ResNet-50 [6], EfficientNet-B0 [8], and MobileNetV2 [7] into a 5,120-dimensional representation, served through a FastAPI backend and a React frontend with inference-time uncertainty logic [9], [10].

Rather than asserting unverified performance figures, this paper provides an honest, evidence-based account of the prototype's current implementation and limitations:
- The prototype is explicitly non-diagnostic and has not undergone clinical validation.
- The repository contains 940 JPEG images (490 cancer, 450 non-cancer) with unverified provenance and no patient-level identifiers.
- A hash audit identified 21 duplicate image groups encompassing 46 individual files (representing 25 redundant copies), including 11 groups (encompassing 25 files, representing 14 redundant copies) that cross partition boundaries, precluding the current test partition from being considered a properly separated or independent test set.
- Training scripts and reproducible training histories are absent, and previously reported benchmark figures (such as 99.92% accuracy) were generated synthetically rather than through empirical model evaluation.
- No empirical evaluation results on the dataset are currently available.

By prioritizing scientific integrity, data transparency, and objective engineering documentation over premature performance assertions, this paper provides a transparent baseline for future academic work.

---

## 10. References

> *Note: Temporary numbered citation format. Specific bibliographic styling (e.g., IEEE, ACM, Springer LNCS) will be applied upon selection of target publication venue.*

[1] H. Sung, J. Ferlay, R. L. Siegel, M. Laversanne, I. Soerjomataram, A. Jemal, and F. Bray, "Global Cancer Statistics 2020: GLOBOCAN Estimates of Incidence and Mortality Worldwide for 36 Cancers in 185 Countries," *CA: A Cancer Journal for Clinicians*, vol. 71, no. 3, pp. 209–249, 2021. DOI: [10.3322/caac.21660](https://doi.org/10.3322/caac.21660).

[2] P. Brocklehurst, O. Kujan, L. A. O'Malley, G. R. Ogden, S. Shepherd, and A.-M. Glenny, "Screening programmes for the early detection and prevention of oral cancer," *Cochrane Database of Systematic Reviews*, no. 11, Art. No. CD004150, 2013. DOI: [10.1002/14651858.CD004150.pub4](https://doi.org/10.1002/14651858.CD004150.pub4).

[3] R. A. Welikala, P. Remagnino, J. H. Lim, C. S. Chan, S. Rajendran, T. G. Kallarakkal, R. B. Zain, R. D. Jayasinghe, V. Mohan, A. Rao, K. A. Amirtham, and S. J. Loffman, "Automated Detection and Classification of Oral Lesions Using Deep Learning for Early Detection of Oral Cancer," *IEEE Access*, vol. 8, pp. 132677–132693, 2020. DOI: [10.1109/ACCESS.2020.3010180](https://doi.org/10.1109/ACCESS.2020.3010180).

[4] K. Warin, W. Limprasert, S. Suebnukarn, S. Jinaporntham, P. Jantana, and S. Vicharueang, "AI-based analysis of oral lesions using novel deep convolutional neural networks for early detection of oral cancer," *PLOS ONE*, vol. 17, no. 8, p. e0273508, 2022. DOI: [10.1371/journal.pone.0273508](https://doi.org/10.1371/journal.pone.0273508).

[5] K. Simonyan and A. Zisserman, "Very Deep Convolutional Networks for Large-Scale Image Recognition," in *3rd International Conference on Learning Representations (ICLR 2015)*, San Diego, CA, USA, 2015. arXiv: [1409.1556](https://arxiv.org/abs/1409.1556).

[6] K. He, X. Zhang, S. Ren, and J. Sun, "Deep Residual Learning for Image Recognition," in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2016, pp. 770–778. DOI: [10.1109/CVPR.2016.90](https://doi.org/10.1109/CVPR.2016.90).

[7] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, "MobileNetV2: Inverted Residuals and Linear Bottlenecks," in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2018, pp. 4510–4520. DOI: [10.1109/CVPR.2018.00474](https://doi.org/10.1109/CVPR.2018.00474).

[8] M. Tan and Q. V. Le, "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks," in *Proceedings of the 36th International Conference on Machine Learning (ICML)*, PMLR, vol. 97, 2019, pp. 6105–6114. Available: [https://proceedings.mlr.press/v97/tan19a.html](https://proceedings.mlr.press/v97/tan19a.html).

[9] Y. Gal and Z. Ghahramani, "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning," in *Proceedings of the 33rd International Conference on Machine Learning (ICML)*, PMLR, vol. 48, 2016, pp. 1050–1059. Available: [https://proceedings.mlr.press/v48/gal16.html](https://proceedings.mlr.press/v48/gal16.html).

[10] M. S. Ayhan and P. Berens, "Test-time Data Augmentation for Estimation of Heteroscedastic Aleatoric Uncertainty in Deep Neural Networks," in *Proceedings of the 1st Conference on Medical Imaging with Deep Learning (MIDL)*, Amsterdam, The Netherlands, 2018. arXiv: [1803.06013](https://arxiv.org/abs/1803.06013).

[11] M. Roberts, D. Driggs, M. Thorpe, J. Gilbey, M. Yeung, S. Ursprung, A. I. Aviles-Rivero, C. Etmann, C. McCague, L. Beer, J. R. Weir-McCall, Z. Teng, E. Gkrania-Klotsas, AIX-COVNET Collaboration, J. H. F. Rudd, E. Sala, and C.-B. Schönlieb, "Common pitfalls and recommendations for using machine learning to detect and prognosticate for COVID-19 using chest radiographs and CT scans," *Nature Machine Intelligence*, vol. 3, no. 3, pp. 199–217, 2021. DOI: [10.1038/s42256-021-00307-0](https://doi.org/10.1038/s42256-021-00307-0).

[12] S. Kapoor and A. Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science," *Patterns*, vol. 4, no. 9, p. 100804, 2023. DOI: [10.1016/j.patter.2023.100804](https://doi.org/10.1016/j.patter.2023.100804).

[13] A. Chattopadhay, A. Sarkar, P. Howlader, and V. N. Balasubramanian, "Grad-CAM++: Generalized Gradient-Based Visual Explanations for Deep Convolutional Networks," in *Proceedings of the IEEE Winter Conference on Applications of Computer Vision (WACV)*, 2018, pp. 839–847. DOI: [10.1109/WACV.2018.00097](https://doi.org/10.1109/WACV.2018.00097).

---

## Author Verification Checklist

Before finalizing this manuscript for academic submission, the author must confirm the following factual items with their project guide, dataset source, or institutional authorities:

- [ ] **Item 1: Dataset Provenance & Permissions:** Identify and document the exact Kaggle dataset source URL, original contributing author/institution, upload date, and verify whether license terms permit academic research publication [TO VERIFY].
- [ ] **Item 2: Ethical / IRB Governance:** Verify whether the dataset collection originally operated under an Institutional Review Board (IRB) or human research ethics committee protocol, and whether patient consent was obtained [TO VERIFY].
- [ ] **Item 3: Patient-Level Identifiers:** Inquire whether patient-level mapping keys or clinical metadata exist to determine if multiple images belong to the same individual [TO VERIFY].
- [ ] **Item 4: Deduplication and Data Sanitization:** Verify the exact resolution of the 21 duplicate groups (encompassing 46 individual files, with 11 cross-partition groups encompassing 25 files) to produce a properly separated, mutually disjoint dataset.
- [ ] **Item 5: Original Training Scripts & Hyperparameters:** Check with project predecessors or archived directories to determine whether the original training code, optimizer settings, learning rate schedule, loss function, and training logs that produced `merged_model.pth` can be recovered [TO VERIFY].
- [ ] **Item 6: Backbones Initialization & Pre-Training:** Confirm whether the backbones in `merged_model.pth` were originally initialized with ImageNet pre-trained weights or trained from scratch [TO VERIFY].
- [ ] **Item 7: Empirical Test Set Evaluation:** Execute a verified empirical evaluation of `merged_model.pth` on a properly separated, deduplicated test set and record true classification metrics (accuracy, sensitivity, specificity, AUROC) [TO VERIFY].
- [ ] **Item 8: End-to-End Runtime Pipeline Verification:** Confirm runtime execution behavior and consistency of the TTA and Monte Carlo dropout uncertainty gating logic during multi-request server operation [TO VERIFY].
- [ ] **Item 9: Institutional Affiliations & Acknowledgments:** Confirm official department and institutional naming, advisor designations, and any college laboratory resources utilized [TO VERIFY].
