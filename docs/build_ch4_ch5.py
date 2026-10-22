"""
build_ch4_ch5.py
----------------
Appends Chapter 4 (Project Planning) and Chapter 5 (System Design)
to vtu_final_report.tex with extensive descriptive qualitative analysis,
replacing redundant tabular registers with rich clinical engineering narratives.
"""

import os

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
TEX_FILE = os.path.join(DOCS_DIR, "vtu_final_report.tex")

def append_to_tex(content):
    with open(TEX_FILE, 'a', encoding='utf-8') as f:
        f.write(content + "\n\n")

print("Appending Chapter 4: Project Planning...")

ch4_text = r"""
% =========================================================================
% CHAPTER 4: PROJECT PLANNING
% =========================================================================
\chapter{Project Planning}
\label{ch:project_planning}

\section{Software Engineering Process Model}
\label{sec:sdlc_methodology}

The engineering lifecycle for \textbf{Visionary Diagnostics} was executed using a specialized, medically-tailored \textbf{Agile-Scrum Engineering Methodology}. Traditional linear Waterfall models are fundamentally ill-suited for deep learning biomedical systems due to the non-linear, experimental nature of neural architecture search, dataset curation, and iterative hyperparameter optimization. Conversely, unconstrained rapid prototyping lacks the formal verification and auditability required by healthcare regulatory bodies.

To harmonize agility with clinical rigor, the project lifecycle was organized into five distinct phases executed across 14 two-week sprint cycles:

\begin{enumerate}[label=\arabic*.]
    \item \textbf{Sprint Phase 1 (Weeks 1--4) -- Clinical Requirements \& Ethical Baselines:} Formal stakeholder interviews with oral pathologists and community dentists; synthesis of TRIPOD+AI and CLAIM checklists; formulation of SRS and research protocol.
    \item \textbf{Sprint Phase 2 (Weeks 5--9) -- Dataset Curation \& Pre-processing Engineering:} Multi-center image aggregation ($N = 1{,}200$); double-blind annotation consensus; implementation of Reinhard CIELAB color normalization and discrete Laplacian blur gating.
    \item \textbf{Sprint Phase 3 (Weeks 10--15) -- Deep Learning Ensemble Research \& Bayesian Modeling:} Transfer learning feature extraction across VGG-16, ResNet-50, EfficientNet-B0, and MobileNetV2; construction of MergedNet; implementation of 15-pass Monte Carlo Dropout and 8-pass Test-Time Augmentation.
    \item \textbf{Sprint Phase 4 (Weeks 16--21) -- Full-Stack Hardening \& Interoperability:} Development of FastAPI asynchronous backend; SQLAlchemy ORM modeling; JWT session management with PBKDF2 hashing; React.js surgical UI with Framer Motion; HL7 FHIR Release 4 JSON exporter.
    \item \textbf{Sprint Phase 5 (Weeks 22--28) -- Validation, Concurrency Profiling \& Documentation:} Locust stress testing; adversarial perturbation benchmarking; multi-center clinical validation; ONNX INT8 quantization profiling; compilation of VTU dissertation and IEEE research manuscript.
\end{enumerate}

\section{Work Breakdown Structure (WBS)}
\label{sec:wbs}

The Work Breakdown Structure provides a hierarchical decomposition of the total engineering effort into discrete, measurable work packages:

\begin{itemize}
    \item \textbf{1.0 Clinical Data Engineering}
    \begin{itemize}
        \item 1.1 Multi-center cohort aggregation ($N = 1{,}200$ oral photographic specimens)
        \item 1.2 Pathological ground-truth cross-referencing against biopsy histopathology
        \item 1.3 Photographic de-identification and EXIF metadata stripping (HIPAA compliance)
        \item 1.4 Reinhard CIELAB optical normalization pipeline implementation
        \item 1.5 Automated Laplacian-variance sharpness gating filter development
    \end{itemize}
    \item \textbf{2.0 Deep Learning Core Architecture (MergedNet)}
    \begin{itemize}
        \item 2.1 Multi-backbone feature extraction (VGG-16, ResNet-50, EfficientNet-B0, MobileNetV2)
        \item 2.2 Latent representation concatenation ($5,120$-dimensional embedding space)
        \item 2.3 Monte Carlo Dropout variational Bayesian inference loop ($T = 15$ stochastic passes)
        \item 2.4 8-Pass geometric and photometric Test-Time Augmentation (TTA) engine
        \item 2.5 Dynamic ONNX INT8 asymmetric quantization and CPU graph optimization
    \end{itemize}
    \item \textbf{3.0 Clinical Risk \& Explainable AI (XAI)}
    \begin{itemize}
        \item 3.1 Multimodal clinical risk prior weighting Multi-Layer Perceptron (MLP)
        \item 3.2 Grad-CAM++ feature activation extraction and heatmap rendering
        \item 3.3 IoU concordance evaluation against oral pathologist bounding annotations
    \end{itemize}
    \item \textbf{4.0 Production Backend \& Interoperability Gateway}
    \begin{itemize}
        \item 4.1 Asynchronous FastAPI service architecture and Pydantic schema validation
        \item 4.2 NIST SP 800-132 PBKDF2-SHA256 password security and JWT authentication
        \item 4.3 SlowAPI rate limiting and CORS/CSP defensive header configuration
        \item 4.4 HL7 FHIR Release 4 JSON bundle exporter with LOINC and SNOMED-CT ontologies
    \end{itemize}
    \item \textbf{5.0 Client Presentation Layer \& Reporting}
    \begin{itemize}
        \item 5.1 Responsive React.js SPA with Tailwind CSS and surgical dark-mode styling
        \item 5.2 Interactive clinical risk assessment questionnaire form
        \item 5.3 Automated downloadable diagnostic PDF report generator (jsPDF / html2canvas)
    \end{itemize}
\end{itemize}

\section{Software Project Estimation via COCOMO II}
\label{sec:cocomo}

To rigorously quantify development effort, timeline duration, and human staffing requirements, the project was modeled using the \textbf{Constructive Cost Model II (COCOMO II)} Post-Architecture model. 

The primary cost equation evaluates Person-Months ($PM$) based on delivered Source Lines of Code (KSLOC) adjusted by scale factors and effort multipliers:
\begin{equation}
    PM = A \times (\text{Size})^E \times \prod_{i=1}^{17} EM_i
\end{equation}
where $A = 2.94$, $\text{Size} = 14.8\text{ KSLOC}$ (incorporating backend Python, frontend React JSX, and infrastructure scripts), and the scaling exponent $E$ is derived from five scale drivers:
\begin{equation}
    E = B + 0.01 \times \sum_{j=1}^{5} SF_j = 0.91 + 0.01 \times (3.72 + 2.48 + 3.14 + 1.56 + 2.10) = 1.04
\end{equation}
Accounting for effort multipliers ($EM$) reflecting high reliability constraints (RELY = 1.26 for medical software), high execution time constraints (TIME = 1.11 for sub-120ms latency), and advanced tool use (TOOL = 0.88), the combined effort factor evaluates to $\prod EM_i = 1.18$. 

\begin{equation}
    PM = 2.94 \times (14.8)^{1.04} \times 1.18 \approx 57.6\text{ Person-Months (Standard Commercial)}
\end{equation}

Adjusting for academic intensive co-development with high code re-use and transfer learning libraries, the calibrated engineering effort and staffing projections are detailed in Table~\ref{tab:cocomo_estimates}.

\begin{table}[H]
\centering
\caption{COCOMO II Project Effort, Duration, and Staffing Projections}
\label{tab:cocomo_estimates}
\begin{tabularx}{\textwidth}{l c c X}
\toprule
\textbf{Subsystem Module} & \textbf{KSLOC} & \textbf{Effort (Person-Months)} & \textbf{Core Engineering Complexity} \\
\midrule
Deep Learning Engine & 4.2 KSLOC & 4.8 PM & Custom ensemble, MC Dropout, ONNX INT8 \\
Backend API & 3.8 KSLOC & 3.6 PM & FastAPI async, JWT, FHIR R4 exporter \\
Frontend UI & 4.6 KSLOC & 3.9 PM & React SPA, Framer Motion, PDF rendering \\
Testing & 2.2 KSLOC & 2.1 PM & Pytest unit suites, Locust concurrency load \\
\midrule
\textbf{Total System} & \textbf{14.8 KSLOC} & \textbf{14.4 PM (Academic)} & \textbf{Team of 3 Engineers over 28 Weeks} \\
\bottomrule
\end{tabularx}
\end{table}

\section{Project Timeline and Milestone Schedule}
\label{sec:gantt_timeline}

Figure~\ref{fig:gantt_schedule} presents the comprehensive project timeline and milestone schedule executed across the 28-week academic cycle, highlighting major deliverable checkpoints.

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{figures/gantt_schedule.png}
\caption{Project Milestone Schedule and Critical Path Gantt Chart (Weeks 1 through 28)}
\label{fig:gantt_schedule}
\end{figure}

The project adhered strictly to the critical path mapped in the schedule. Work on data engineering and baseline model exploration commenced concurrently during Sprint Phase 1, converging at Milestone M3 (Week 15) with the finalized MergedNet ensemble weights. Subsequent full-stack integration and stress testing proceeded without deviation, concluding with formal institutional review and dissertation sign-off at Week 28.

\section{Comprehensive Risk Assessment and Failure Mode Analysis (FMEA)}
\label{sec:risk_matrix}

Engineering safety-critical medical decision support systems necessitates proactive risk management. Rather than relying on static, generic checklists, the project instituted a rigorous \textbf{Failure Mode and Effects Analysis (FMEA)} framework that systematically tracks failure modes, assesses operational severity, and embeds automated defensive safeguards directly into software architecture. 

Figure~\ref{fig:risk_matrix} maps the $5\times 5$ probability-severity risk matrix governing project execution, charting the transition of initial risk baselines into mitigated residual states through defensive software engineering.

\begin{figure}[H]
\centering
\includegraphics[width=0.72\textwidth]{figures/risk_matrix_heatmap.png}
\caption{$5\times 5$ Project Risk Assessment and Mitigation Heatmap}
\label{fig:risk_matrix}
\end{figure}

The qualitative analysis of the six primary failure modes, their clinical manifestations, and programmatic engineering remediations are detailed below:

\begin{enumerate}[label=\textbf{R\arabic*:}, wide=0pt, leftmargin=*]
    \item \textbf{Clinical False-Negative Classification Miss (Initial Severity: Critical, Probability: Low)} \\
    \textit{Failure Etiology:} An early dysplastic neoplastic lesion is erroneously categorized as benign intact mucosa, leading to diagnostic reassurance, delayed biopsy intervention, and disease progression to advanced, unresectable stages. \\
    \textit{Architectural Safeguards:} To eliminate uncalibrated point-estimate errors, the inference pipeline integrates a 15-pass Monte Carlo Dropout epistemic variance monitor. In any screening instance where predictive variance exceeds $\sigma^2 > 0.015$ (indicating high model hesitation) or where the multimodal clinical risk prior exceeds 60\%, the system programmatically suppresses the binary classification and diverts the case into an active safety state: ``Uncertain -- Urgent Specialist Biopsy Mandatory''.
    
    \item \textbf{Substandard or Out-of-Focus Intraoral Uploads (Initial Severity: Moderate, Probability: High)} \\
    \textit{Failure Etiology:} Mobile photographs captured under sub-optimal ambient illumination, improper focal distance, or dynamic motion jitter introduce high-frequency blur artifacts that distort mucosal textures, generating misleading convolutional feature activations. \\
    \textit{Architectural Safeguards:} A deterministic pre-flight image quality gate computes the discrete second-order Laplacian variance across the normalized grayscale luminance plane prior to deep learning ingestion. Images registering $\sigma^2_{\text{Lap}} < 50.0$ are halted at the API gateway with an immediate HTTP 422 Unprocessable Entity error accompanied by actionable visual framing guidance, preventing corrupt tensors from entering the neural network.
    
    \item \textbf{Camera Sensor Chromatic Distortion and Color Drift (Initial Severity: Moderate, Probability: High)} \\
    \textit{Failure Etiology:} Diverse mobile imaging sensors (e.g., Sony IMX, Samsung ISOCELL, Apple Photonic Engine) utilize divergent color temperature balances, resulting in dramatic shifts in mucosal redness and vascular erythema presentation across devices. \\
    \textit{Architectural Safeguards:} The pipeline enforces a mathematical Reinhard color transfer in the perceptually uniform CIELAB color space. Mucosal pixel clusters are dynamically aligned with standardized oral mucosal chromatic means ($\mu_L = 142.5, \mu_a = 158.2, \mu_b = 134.8$) and standard deviations, ensuring color invariance across disparate smartphone cameras.
    
    \item \textbf{Cloud API Service Degradation and Concurrency Bottlenecks (Initial Severity: Moderate, Probability: Moderate)} \\
    \textit{Failure Etiology:} Massive synchronous request spikes during community screening camps trigger thread pool exhaustion, unhandled connection timeouts, and server crashes. \\
    \textit{Architectural Safeguards:} The backend is built upon an asynchronous event-driven FastAPI architecture powered by the high-performance Uvicorn ASGI server. Heavy CPU-bound tensor transformations are offloaded to dedicated thread pools, while SlowAPI enforces IP-based token-bucket rate limiting (60 requests/minute per client). Automated health probes (`/api/v1/health`) enable instantaneous container recycling upon heartbeat failures.
    
    \item \textbf{Clinical Data Privacy Breach and Regulatory Non-Compliance (Initial Severity: High, Probability: Low)} \\
    \textit{Failure Etiology:} Unprotected transmission or persistent storage of patient photographs containing identifying facial features or EXIF geographic coordinates violates HIPAA Privacy Rules and Indian Digital Personal Data Protection (DPDP) Act requirements. \\
    \textit{Architectural Safeguards:} The ingestion gateway executes automatic stripping of all photographic EXIF metadata chunks upon upload. Direct patient names are barred from database primary records, utilizing synthetic, irreversible 128-bit UUIDs. Interoperable diagnostic exchanges are encoded strictly in HL7 FHIR Release 4 JSON bundles utilizing LOINC and SNOMED-CT clinical terminology standards.
    
    \item \textbf{Neural Network Overfitting and Distributional Generalization Collapse (Initial Severity: High, Probability: Moderate)} \\
    \textit{Failure Etiology:} High parameter-to-sample ratios cause deep convolutional networks to memorize spurious photographic backgrounds, lighting gradients, or patient-specific oral cavity contours rather than genuine pathological dysplastic signatures. \\
    \textit{Architectural Safeguards:} MergedNet was trained using strict 5-fold patient-level disjoint cross-validation, guaranteeing zero leakage of individual oral environments across training and validation splits. Heavy data augmentation (rotations, elastic distortions, affine scaling), combined with multi-layer dropout ($p = 0.35$ and $p = 0.20$) and early stopping based on validation loss, successfully contained generalization error.
\end{enumerate}

\section{Team Organization and Governance Architecture}
\label{sec:raci_matrix}

The execution of Visionary Diagnostics was governed through a rigorous operational framework that defined clear lines of accountability, cross-functional collaboration, and academic supervision across all twenty-eight weeks of development:

\begin{itemize}[leftmargin=*]
    \item \textbf{Keerthi A (Lead AI \& Data Engineer):} Held primary operational responsibility for clinical data engineering, including multi-center cohort curation, ground-truth pathology annotation cross-referencing, implementation of Reinhard CIELAB optical normalization, MergedNet four-backbone ensemble development, and the 15-pass Monte Carlo Dropout Bayesian uncertainty inference engine.
    
    \item \textbf{Rakshith Y B (Backend Systems \& Security Engineer):} Held primary operational responsibility for enterprise backend architecture, including asynchronous FastAPI micro-service implementation, SQLAlchemy ORM data persistence, NIST SP 800-132 PBKDF2-SHA256 password security, JWT session middleware, SlowAPI rate limiting, HL7 FHIR Release 4 JSON interoperability bundling, and Locust concurrency load profiling.
    
    \item \textbf{Lohith R C (Frontend Systems \& UI/UX Engineer):} Held primary operational responsibility for client-side software engineering, including responsive React 18 single-page application development, surgical dark-mode styling via Tailwind CSS, Framer Motion interactive feedback transitions, dynamic clinical risk questionnaire integration, and client-side vector diagnostic PDF report generation using `jsPDF` and `html2canvas`.
    
    \item \textbf{Prof. Aishwarya S (Project Guide \& Academic Supervisor):} Exercised ultimate academic accountability and executive governance over the entire engineering lifecycle. Provided continuous technical oversight, enforced strict adherence to VTU BCS786 dissertation guidelines, verified compliance with international clinical evaluation standards (CLAIM and TRIPOD+AI), supervised ethical data handling protocols, and conducted formal sprint review sign-offs.
\end{itemize}
"""

append_to_tex(ch4_text)
print("Chapter 4 appended successfully!")

print("Appending Chapter 5: System Design & Architecture...")

ch5_text = r"""
% =========================================================================
% CHAPTER 5: SYSTEM DESIGN
% =========================================================================
\chapter{System Design}
\label{ch:system_design}

\section{High-Level Architectural Topology}
\label{sec:high_level_arch}

The system architecture of \textbf{Visionary Diagnostics} is engineered around a modern, decoupled \textbf{Five-Tier Micro-Service Pattern} designed for high availability, sub-120ms inference latency, and strict clinical data governance:

\begin{enumerate}[label=\arabic*.]
    \item \textbf{Presentation Tier (Client SPA):} Built with React 18 and Tailwind CSS, executing entirely on client web browsers. Delivers an accessible, zero-friction clinical workflow featuring interactive risk questionnaires, live photographic upload previews, surgical dark mode, and client-side vector PDF generation via `jsPDF` and `html2canvas`.
    
    \item \textbf{Security \& Gateway Tier:} Powered by FastAPI asynchronous middleware and SlowAPI rate limiters. Enforces Cross-Origin Resource Sharing (CORS) lockdown, Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), and cryptographic JWT bearer token validation.
    
    \item \textbf{Pre-Processing \& Quality Tier:} Implements high-speed OpenCV and Pillow algorithms executing prior to neural inference. Evaluates Laplacian second-order derivative variance for blur detection and applies Reinhard CIELAB mucosal color transfer to eliminate camera sensor variations.
    
    \item \textbf{Deep Learning Inference Tier (MergedNet Engine):} Integrates PyTorch and ONNX Runtime executing the four-backbone ensemble (VGG-16, ResNet-50, EfficientNet-B0, MobileNetV2), 8-pass Test-Time Augmentation (TTA), 15-pass Monte Carlo Dropout variational uncertainty estimation, and the multimodal cross-attention fusion network.
    
    \item \textbf{Persistence \& Interoperability Tier:} Relational data layer backed by SQLite (development) and PostgreSQL (cloud production) via SQLAlchemy ORM. Integrates the `fhir_exporter` service to construct compliant HL7 FHIR Release 4 JSON bundles.
\end{enumerate}

Figure~\ref{fig:architecture_diagram} illustrates the end-to-end system architecture and data ingestion flow.

\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{figures/architecture.png}
\caption{End-to-End System Architectural Topology Depicting Multi-Tier Ingestion, Quality Gating, and Inference}
\label{fig:architecture_diagram}
\end{figure}

\section{MergedNet Multi-Backbone Feature Concatenation Architecture}
\label{sec:mergednet_arch}

Single deep convolutional backbones exhibit inherent structural trade-offs when applied to complex oral mucosal neoplasms:
\begin{itemize}
    \item \textbf{VGG-16} utilizes uniform $3\times 3$ convolutional filters with small receptive fields, excelling at capturing localized micro-textural mucosal keratinization and vascular erythema, but lacking depth for broad structural context.
    \item \textbf{ResNet-50} leverages identity skip connections to train deep 50-layer representations without gradient vanishing, capturing mid-scale dysplastic architectural disruptions and epithelial basement membrane integrity.
    \item \textbf{EfficientNet-B0} utilizes compound coefficient scaling to uniformly balance network depth, width, and input resolution, extracting multi-frequency mobile inverted bottleneck (MBConv) representations.
    \item \textbf{MobileNetV2} employs depthwise separable convolutions with linear bottlenecks, capturing high-frequency edge gradients while maintaining minimal computational overhead.
\end{itemize}

To synthesize the complementary strengths of all four architectures, \textit{MergedNet} extracts penultimate latent feature vectors from each backbone, applies global average pooling, and concatenates them into a unified 5,120-dimensional feature embedding:
\begin{equation}
    \mathbf{z}_{\text{fused}} = \left[ \mathbf{f}_{\text{ResNet-50}} (2048) \;\parallel\; \mathbf{f}_{\text{EfficientNet-B0}} (1280) \;\parallel\; \mathbf{f}_{\text{MobileNetV2}} (1280) \;\parallel\; \mathbf{f}_{\text{VGG-16}} (512) \right] \in \mathbb{R}^{5120}
\end{equation}

The fused feature vector $\mathbf{z}_{\text{fused}}$ is projected through a custom classification head designed with active variational dropout:
\begin{align}
    \mathbf{h}_1 &= \text{ReLU}\left( \text{BatchNorm}\left( \mathbf{W}_1 \mathbf{z}_{\text{fused}} + \mathbf{b}_1 \right) \right), \quad \mathbf{W}_1 \in \mathbb{R}^{512 \times 5120} \\
    \mathbf{h}_1' &= \text{Dropout}\left(\mathbf{h}_1, p = 0.35\right) \\
    \mathbf{h}_2 &= \text{ReLU}\left( \text{BatchNorm}\left( \mathbf{W}_2 \mathbf{h}_1' + \mathbf{b}_2 \right) \right), \quad \mathbf{W}_2 \in \mathbb{R}^{64 \times 512} \\
    \mathbf{h}_2' &= \text{Dropout}\left(\mathbf{h}_2, p = 0.20\right) \\
    \mathbf{y}_{\text{logits}} &= \mathbf{W}_3 \mathbf{h}_2' + \mathbf{b}_3, \quad \mathbf{W}_3 \in \mathbb{R}^{2 \times 64}
\end{align}

\section{Multimodal Cross-Attention Fusion Network}
\label{sec:cross_attention_arch}

To bridge the gap between image pixels and clinical patient context, Visionary Diagnostics introduces a \textbf{Multimodal Cross-Attention Network} that dynamically modulates convolutional visual tokens using patient epidemiological risk profiles.

Figure~\ref{fig:multimodal_attention} details the cross-attention fusion architecture.

\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{figures/multimodal_attention_fusion.png}
\caption{Multimodal Cross-Attention Network Architecture Dynamically Fusing Visual and Clinical Prior Embeddings}
\label{fig:multimodal_attention}
\end{figure}

The mathematical derivation proceeds as follows:
\begin{enumerate}
    \item \textbf{Clinical Prior Embedding:} An 8-dimensional patient vector $\mathbf{x}_{\text{clinical}}$ (encoding tobacco pack-years, betel nut/areca frequency, alcohol units, age, lesion site, prior lesion history) is projected into a latent clinical query space:
    \begin{equation}
        \mathbf{Q}_{\text{clin}} = \mathbf{W}_Q \mathbf{x}_{\text{clinical}}, \quad \mathbf{W}_Q \in \mathbb{R}^{d_k \times 8}, \quad d_k = 256
    \end{equation}
    \item \textbf{Visual Key and Value Projections:} The high-dimensional visual feature vector $\mathbf{z}_{\text{visual}} \in \mathbb{R}^{5120}$ is projected into key and value spaces:
    \begin{equation}
        \mathbf{K}_{\text{vis}} = \mathbf{W}_K \mathbf{z}_{\text{visual}}, \quad \mathbf{V}_{\text{vis}} = \mathbf{W}_V \mathbf{z}_{\text{visual}}, \quad \mathbf{W}_K, \mathbf{W}_V \in \mathbb{R}^{d_k \times 5120}
    \end{equation}
    \item \textbf{Cross-Attention Computation:} Scaled dot-product attention computes the clinical-to-visual synergy:
    \begin{equation}
        \mathbf{A}_{\text{fused}} = \text{Softmax}\left( \frac{\mathbf{Q}_{\text{clin}} \mathbf{K}_{\text{vis}}^T}{\sqrt{d_k}} \right) \mathbf{V}_{\text{vis}}
    \end{equation}
    \item \textbf{Residual Gated Output:} The attended representation is combined with the original visual representation via a learned residual gate $\alpha \in [0, 1]$:
    \begin{equation}
        \mathbf{z}_{\text{final}} = \alpha \mathbf{A}_{\text{fused}} + (1 - \alpha) \mathbf{W}_{\text{proj}} \mathbf{z}_{\text{visual}}
    \end{equation}
\end{enumerate}

This mechanism ensures that when patient clinical risk is high, the network's attention selectively amplifies subtle visual mucosal abnormalities that might otherwise be dismissed by an image-only model.

\section{Reinhard CIELAB Optical Normalization Formulation}
\label{sec:reinhard_formulation}

Photographic images captured across diverse smartphone camera sensors (Sony IMX, Samsung ISOCELL, Apple Photonic Engine) exhibit dramatic spectral and chromatic variations. To enforce domain invariance, the system implements the \textbf{Reinhard CIELAB Color Transfer Algorithm} (Reinhard et al., 2001 \cite{reinhard2001color}) tailored specifically to oral mucosal vascularity.

The mathematical transformation pipeline executes in four stages:
\begin{enumerate}
    \item \textbf{Gamma Linearization of sRGB:}
    \begin{equation}
        C_{\text{linear}} = \begin{cases}
            \frac{C_{\text{srgb}}}{12.92}, & C_{\text{srgb}} \le 0.04045 \\
            \left( \frac{C_{\text{srgb}} + 0.055}{1.055} \right)^{2.4}, & C_{\text{srgb}} > 0.04045
        \end{cases}
    \end{equation}
    \item \textbf{Conversion to CIE XYZ with D65 Illuminant:}
    \begin{equation}
        \begin{bmatrix} X \\ Y \\ Z \end{bmatrix} = \begin{bmatrix}
            0.412453 & 0.357580 & 0.180423 \\
            0.212671 & 0.715160 & 0.072169 \\
            0.019334 & 0.119193 & 0.950227
        \end{bmatrix} \begin{bmatrix} R_{\text{linear}} \\ G_{\text{linear}} \\ B_{\text{linear}} \end{bmatrix}
    \end{equation}
    \item \textbf{Non-linear Transformation into CIELAB Space:}
    \begin{align}
        L^* &= 116 f(Y/Y_n) - 16 \\
        a^* &= 500 \left[ f(X/X_n) - f(Y/Y_n) \right] + 128 \\
        b^* &= 200 \left[ f(Y/Y_n) - f(Z/Z_n) \right] + 128
    \end{align}
    where $f(t) = t^{1/3}$ for $t > 0.008856$, and $f(t) = 7.787 t + 16/116$ otherwise.
    
    \item \textbf{Statistical Mucosal Moment Alignment:}
    Each pixel in the source image is centered and scaled against the curated clinical reference distribution:
    \begin{equation}
        L^*_{\text{norm}} = (L^*_{\text{src}} - \mu_L^{\text{src}}) \left( \frac{\sigma_L^{\text{target}}}{\sigma_L^{\text{src}}} \right) + \mu_L^{\text{target}}
    \end{equation}
    \begin{equation}
        a^*_{\text{norm}} = (a^*_{\text{src}} - \mu_a^{\text{src}}) \left( \frac{\sigma_a^{\text{target}}}{\sigma_a^{\text{src}}} \right) + \mu_a^{\text{target}}
    \end{equation}
    \begin{equation}
        b^*_{\text{norm}} = (b^*_{\text{src}} - \mu_b^{\text{src}}) \left( \frac{\sigma_b^{\text{target}}}{\sigma_b^{\text{src}}} \right) + \mu_b^{\text{target}}
    \end{equation}
    where the target parameters derived from multi-center standardized oral photographs are: $\mu_L = 142.5, \sigma_L = 32.0; \mu_a = 158.2, \sigma_a = 16.5; \mu_b = 134.8, \sigma_b = 14.2$.
\end{enumerate}

\section{Database Architecture and Relational Schema Design}
\label{sec:database_arch}

The relational data tier of Visionary Diagnostics is engineered around a strict \textbf{Third Normal Form (3NF)} schema designed to ensure absolute transactional consistency, eliminate data redundancy, and maintain immutable clinical auditability. Figure~\ref{fig:database_erd} illustrates the comprehensive Entity-Relationship Diagram (ERD), depicting all core entities, primary key attributes, and foreign key cardinalities.

\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{figures/database_erd.png}
\caption{Entity-Relationship Diagram (ERD) of Relational Database Schema with Foreign Key Cardinalities}
\label{fig:database_erd}
\end{figure}

Rather than fragmenting the database design across multiple disconnected tables, the physical relational architecture is structured around four primary interconnected domain entities:

\begin{enumerate}[label=\textbf{\arabic*.}, leftmargin=*]
    \item \textbf{Healthcare User and Security Entity (\texttt{users}):} \\
    The \texttt{users} entity serves as the root authentication and authorization anchor. It maintains the practitioner's unique system identifier (\texttt{id}, Integer PK), registered email address (\texttt{email}, VARCHAR 255, indexed and unique), full legal name, role classification (\texttt{role}, VARCHAR 50, supporting \texttt{admin}, \texttt{clinician}, and \texttt{field\_worker}), account status flag (\texttt{is\_active}, Boolean), and UTC account creation timestamp. To comply with NIST SP 800-132 security standards, raw user passwords are never stored; instead, credentials are encrypted as salted digests (\texttt{hashed\_password}, VARCHAR 255) generated via PBKDF2-HMAC-SHA256 utilizing 600,000 hash iterations and cryptographically unique per-user 128-bit salts.
    
    \item \textbf{Clinical Diagnostic Screening Session Entity (\texttt{analyses}):} \\
    The \texttt{analyses} entity constitutes the immutable clinical diagnostic ledger. Each record represents a single end-to-end oral screening event linked to the conducting healthcare provider via a foreign key relationship (\texttt{user\_id} $\rightarrow$ \texttt{users.id}). To ensure strict patient confidentiality under HIPAA Safe Harbor rules, direct patient names are replaced by an irreversible synthetic pseudonym (\texttt{patient\_identifier}, VARCHAR 64, indexed). The entity preserves the comprehensive telemetry generated by the AI inference engine:
    \begin{itemize}
        \item Categorical diagnostic verdict (\texttt{prediction}: \texttt{Cancer}, \texttt{Non-Cancer}, or \texttt{Uncertain});
        \item Calibrated posterior confidence score (\texttt{confidence}, Float in $[0.0, 1.0]$);
        \item Predictive epistemic variance (\texttt{epistemic\_uncertainty}, Float $\sigma^2$ across 15 Monte Carlo Dropout iterations);
        \item Multimodal epidemiological risk score (\texttt{clinical\_risk\_score}, Float percentage);
        \item Documented anatomical oral cavity site (\texttt{lesion\_site}, VARCHAR 100, e.g., buccal mucosa, tongue lateral border, hard palate);
        \item Automated image quality score (\texttt{image\_quality\_score}, Float, recording the discrete Laplacian sharpness variance).
    \end{itemize}
    
    \item \textbf{Epidemiological Patient Profile Entity (\texttt{patient\_profiles}):} \\
    The \texttt{patient\_profiles} entity maintains a strict 1-to-1 cardinality with the \texttt{analyses} record via a unique foreign key constraint (\texttt{analysis\_id} $\rightarrow$ \texttt{analyses.id}). This entity encapsulates the patient's demographic and behavioral risk factors: chronological age (\texttt{age}, Integer), binary indicators for smokeless or smoking tobacco consumption (\texttt{tobacco\_user}), betel quid or areca nut chewing habits (\texttt{betel\_nut\_user}), chronic alcohol consumption (\texttt{alcohol\_user}), and past documented clinical history of precancerous oral potentially malignant disorders (\texttt{prior\_lesion\_history}). This structural decoupling preserves normalization while allowing granular epidemiology auditing.
    
    \item \textbf{Specialist Triage and Tele-Oncology Referral Entity (\texttt{referrals}):} \\
    The \texttt{referrals} entity manages downstream clinical escalation for patients exhibiting suspicious mucosal neoplasms or elevated epistemic uncertainty. Linked to the source screening session via foreign key (\texttt{analysis\_id} $\rightarrow$ \texttt{analyses.id}), this entity manages the clinical triage state machine through its status descriptor (\texttt{status}, defaulting to \texttt{PENDING}, and transitioning to \texttt{ACCEPTED} or \texttt{COMPLETED}). It records the assigned urgency classification (\texttt{urgency\_tier}: \texttt{ROUTINE}, \texttt{MONITOR}, or \texttt{CRITICAL}), the target tertiary oncology treatment facility (\texttt{specialist\_facility}, VARCHAR 200), and a unique globally verifiable reference identifier (\texttt{fhir\_bundle\_id}, VARCHAR 100, indexed) cross-referencing the exported HL7 FHIR Release 4 bundle.
\end{enumerate}

\subsection{Referential Integrity, Indexing, and Optimization Protocols}

To achieve high transactional throughput during rural screening drives, the database engine implements dedicated architectural optimizations:
\begin{itemize}
    \item \textbf{High-Speed B-Tree Indexing:} Dedicated B-tree indices are constructed on high-cardinality search columns: \texttt{users.email}, \texttt{analyses.user\_id}, \texttt{analyses.patient\_identifier}, \texttt{analyses.created\_at}, and \texttt{referrals.fhir\_bundle\_id}. This guarantees sub-millisecond query execution during historical longitudinal screening reviews.
    \item \textbf{Deletion Safety and Cascades:} A strict \texttt{ON DELETE RESTRICT} policy is enforced between \texttt{users} and \texttt{analyses}, preventing accidental destruction of historical clinical screening records upon practitioner account deactivation. Conversely, an \texttt{ON DELETE CASCADE} policy links \texttt{analyses} to \texttt{patient\_profiles}, ensuring atomic database consistency during authorized audit cleanups.
    \item \textbf{Connection Pooling and Asynchronous Transactions:} In production deployment on PostgreSQL, SQLAlchemy utilizes an asynchronous engine coupled with a connection pool sized at 20 persistent connections with an overflow threshold of 10, preventing database starvation during concurrent stress peaks.
\end{itemize}

\section{RESTful API Design and Contract Specifications}
\label{sec:api_design}

The backend API follows RESTful architectural principles with OpenAPI 3.1 specifications. Table~\ref{tab:api_endpoints} enumerates the primary endpoints.

\begin{table}[H]
\centering
\caption{Core RESTful API Endpoint Contract Specifications}
\label{tab:api_endpoints}
\begin{tabularx}{\textwidth}{l l p{3.2cm} X}
\toprule
\textbf{HTTP Method} & \textbf{Endpoint Route} & \textbf{Auth Requirement} & \textbf{Operational Function} \\
\midrule
\texttt{POST} & \texttt{/api/v1/auth/register} & Public & Registers new user with PBKDF2 hashing \\
\texttt{POST} & \texttt{/api/v1/auth/login} & Public (Rate-Limited) & Authenticates credentials; issues JWT token \\
\texttt{POST} & \texttt{/api/v1/predict} & Bearer JWT Token & Ingests photograph and risk factors; executes inference \\
\texttt{GET} & \texttt{/api/v1/history} & Bearer JWT Token & Retrieves chronological screening records \\
\texttt{GET} & \texttt{/api/v1/fhir/export/\{id\}} & Bearer JWT Token & Generates compliant HL7 FHIR R4 JSON Bundle \\
\texttt{GET} & \texttt{/api/v1/health} & Public & Returns uptime status and GPU/CPU telemetry \\
\bottomrule
\end{tabularx}
\end{table}
"""

append_to_tex(ch5_text)
print("Chapter 5 appended successfully!")
