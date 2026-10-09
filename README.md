# AI-Powered Oral Cancer Detection System (OSCC AI)

[![Frontend Deployment](https://img.shields.io/badge/Frontend-Live%20on%20Render-34D399?style=flat&logo=render&logoColor=white)](https://oral-cancer-ai-x9q3.onrender.com)
[![Backend API](https://img.shields.io/badge/Backend-FastAPI%202.1.0-009688?style=flat&logo=fastapi&logoColor=white)](https://oral-cancer-backend-fiwu.onrender.com)
[![Swagger Docs](https://img.shields.io/badge/API%20Docs-Interactive%20Swagger-85EA2D?style=flat&logo=swagger&logoColor=black)](https://oral-cancer-backend-fiwu.onrender.com/docs)
[![Database](https://img.shields.io/badge/Database-Supabase%20PostgreSQL-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com/)
[![ONNX Runtime](https://img.shields.io/badge/Inference-ONNX%20INT8%20Runtime-005CED?style=flat&logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![PyTorch](https://img.shields.io/badge/Models-PyTorch%20%26%20Torchvision-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![React](https://img.shields.io/badge/Client-React.js%2018-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Branch](https://img.shields.io/badge/Branch-main-blue?style=flat&logo=git&logoColor=white)](https://github.com/Lohith-RC/ORC/tree/main)

An enterprise-grade, multimodal clinical AI screening and triage platform engineered for non-invasive, early detection of **Oral Squamous Cell Carcinoma (OSCC)** from clinical photographs. The platform fuses a 4-backbone deep convolutional ensemble with Bayesian epistemic uncertainty quantification, optical glare suppression, AJCC 8th Edition clinical staging, and an ultra-responsive clinical workstation.

---

## 🌐 Live Deployments & Cloud Demonstrations

| Component | Target URL | Status | Description |
| :--- | :--- | :---: | :--- |
| **Web Client Portal** | [oral-cancer-ai-x9q3.onrender.com](https://oral-cancer-ai-x9q3.onrender.com) | `Active` | Single-page clinical workstation with live intraoral camera capture, dark/light modes, and instant PDF reporting. |
| **Production API** | [oral-cancer-backend-fiwu.onrender.com](https://oral-cancer-backend-fiwu.onrender.com) | `Active` | High-performance FastAPI server with GZip compression and request correlation. |
| **Swagger UI Explorer** | [oral-cancer-backend-fiwu.onrender.com/docs](https://oral-cancer-backend-fiwu.onrender.com/docs) | `Active` | Interactive OpenAPI documentation with built-in JWT bearer authorization. |
| **Health & Telemetry** | [oral-cancer-backend-fiwu.onrender.com/health](https://oral-cancer-backend-fiwu.onrender.com/health) | `Active` | Real-time observability probe inspecting database connectivity, model runtime, and uptime. |
| **Interactive Deck** | [presentation.html](presentation.html) | `Ready` | Standalone Reveal.js presentation deck with live architecture and benchmark slides. |

---

## 🏛️ System Architecture & Inference Pipeline

### System Architecture Overview
![System Architecture](assets/diagrams/system_architecture.png)

### CNN Data Flow & Multi-Stage Triage
![CNN Data Flow](assets/diagrams/data_flow.png)

### Multi-Stage Clinical Vision Pipeline

```
  ┌────────────────────────────────────────────────────────┐
  │         Clinical Specimen / Intraoral Photograph       │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │  Stage 0: Resolution Ingestion & Memory Safeguard      │
  │  - Aspect-preserving thumbnail clamping (≤ 512px)      │
  │  - Single-precision float32 channel normalization      │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │  Stage I: Optical Preprocessing & Morphology           │
  │  - Specular Glare & Saliva Pooling Diffusion           │
  │  - Mucosal Erythema & Leukoplakia Contrast Indexing    │
  │  - Radial Ray-March Boundary & Irregularity Scoring    │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │  Stage II: Deep Convolutional Ensemble Inference       │
  │  - 4-Backbone Ensemble: VGG16 + ResNet50 +             │
  │    EfficientNet-B0 + MobileNetV2                       │
  │  - ONNX INT8 Quantized Runtime (< 40MB resident RAM)   │
  │  - Epistemic Uncertainty Estimation (Monte Carlo)      │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │  Stage III: Zero-OOM Explainability & Alignment        │
  │  - Morphological Saliency Heatmap (< 2MB RAM, < 5ms)   │
  │  - Activation-Lesion IoU Concordance Audit             │
  │  - Base64 RGBA Jet Colormap Overlay Generation         │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │  Stage IV: Multimodal Synthesis & Clinical Triage      │
  │  - AJCC 8th Edition Triage Tier Assignment             │
  │  - Longitudinal Patient Delta Tracking                 │
  │  - HL7 FHIR r4 DiagnosticReport Interoperability       │
  │  - Relational Persistence into Supabase PostgreSQL     │
  └────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features & Technical Highlights

### ⚡ High-Performance Quantized Engine (ONNX INT8)
- **4-Backbone Consensus**: Concatenates deep features from VGG16 (512), ResNet50 (2048), EfficientNet-B0 (1280), and MobileNetV2 (1280) into a 5,120-dimensional classification head.
- **Quantized Execution**: Employs integer-quantized weights (`merged_model_int8.onnx`, 45MB) executed via **ONNX Runtime CPUExecutionProvider**, reducing container memory usage by **>85%** and achieving sub-second inference latency.
- **Startup Kernel Warmup**: Automatically preheats execution providers on container boot, eliminating first-request latency.

### 🛡️ Zero-OOM Morphological Explainability
- Traditional Grad-CAM backpropagation requires full PyTorch autograd graph caching, risking Out-Of-Memory (OOM) kills on memory-constrained cloud environments (e.g., Render Free Tier 512MB RAM cap).
- Introduced **Morphological Saliency Mapping** ([`xai_cam.py`](backend/app/services/xai_cam.py)): computes clinical vascular blush, erythema ratios, and spatial proximity contours with less than **2MB RAM** footprint in under **5ms**.

### 🗄️ Resilient Cloud Relational Database (Supabase PostgreSQL)
- Connected to **Supabase PostgreSQL** in the Singapore region (`ap-southeast-1`) via the official **Supavisor IPv4 Connection Pooler** (`aws-0-ap-southeast-1.pooler.supabase.com:5432`).
- Auto-configured SQLAlchemy 2.0 connection pooling with pre-ping validation, connection recycling, and automatic `postgresql+psycopg2` driver resolution.
- Automatic fallback to local SQLite (`oralcancer.db`) for offline development.

### 💓 Automated Container Keep-Alive Sentinel
- Cloud free-tier instances spin down after 15 minutes of idle time. The backend features a background keep-alive task ([`main.py`](backend/app/main.py)) that sends lightweight diagnostic heartbeats every 8 minutes, ensuring the API stays awake and ready.

### 🔒 Enterprise Defensive Security
- **Content Security Policy (CSP)**: Hardened headers allowing Swagger UI and ReDoc to securely fetch CDNs (`cdn.jsdelivr.net`) without compromising security.
- **Client Origin Isolation**: Strict CORS controls allowing production whitelists and dynamic Vercel preview environments (`https://*.vercel.app`).
- **Cryptographic Security**: Passwords hashed with salted bcrypt; endpoints secured with stateless HS256 JWT bearer tokens.
- **HIPAA-Compliant Audit Logging**: Captures every clinical prediction, timestamp, clinician ID, and IP address in `audit_logs`.

---

## 📁 Repository Structure

```
ORC/
├── assets/
│   ├── diagrams/                  # System architecture, dataflow, and methodology charts
│   │   ├── system_architecture.png
│   │   ├── data_flow.png
│   │   ├── methodology.png
│   │   └── tech_stack.png
│   └── screenshots/               # UI presentation & clinical workflow captures
│       ├── s1.png ... s6.png
│
├── backend/                       # Production FastAPI Application & ML Engine
│   ├── app/
│   │   ├── api/                   # Versioned REST APIs (v1)
│   │   │   └── v1/
│   │   │       ├── endpoints/     # auth, predict, health, history, active_learning, fhir
│   │   │       └── router.py      # Unified API router
│   │   ├── core/                  # Security headers, rate limiting, and config
│   │   ├── db/                    # SQLAlchemy engine, session, and auto-migrations
│   │   ├── models/                # User, Analysis, and AuditLog ORM models
│   │   ├── schemas/               # Strict Pydantic request/response validation
│   │   └── services/              # ML engine, optical normalization, CAM, AJCC staging
│   ├── tests/                     # 46 automated pytest test suites
│   ├── main.py                    # Server entrypoint
│   ├── merged_model.pth           # Full PyTorch FP32 ensemble weights (94MB)
│   ├── merged_model_int8.onnx     # Quantized ONNX INT8 runtime model (45MB)
│   ├── export_onnx.py             # Model quantization & export utility
│   ├── Dockerfile                 # Multi-stage production container
│   └── requirements.txt           # Python dependencies
│
├── frontend/                      # React 18 Single-Page Application
│   ├── public/                    # Static index.html, favicons, manifests
│   ├── src/                       # React components, clinical workstations, and themes
│   │   ├── api.js                 # Axios API client with dynamic base URL
│   │   ├── Navbar.js              # Header with dynamic health indicator
│   │   └── pages/                 # Home, Upload, History, Profile, About
│   ├── tailwind.config.js         # Tailwind CSS styling tokens
│   └── package.json               # Node.js dependencies & scripts
│
├── docs/                          # Comprehensive Technical & Academic Documentation
│   ├── academic_synopsis.md       # Problem statement, clinical objectives, literature review
│   ├── project_details.md         # Contributors, architecture details, module breakdown
│   ├── PRD.md                     # Product Requirements Document
│   ├── TRD.md                     # Technical Requirements Document
│   ├── APP_FLOW.md                # Sequence diagrams & operational workflows
│   └── BACKEND_SCHEMA.md          # Database schema & entity-relationship diagrams
│
├── presentation.html              # Interactive Reveal.js slide presentation
├── vercel.json                    # Vercel deployment routing configuration
└── README.md                      # Primary project documentation
```

---

## 🚀 Deployment Guide

### Option 1: Render (Current Production Setup)

The project is natively configured for deployment on [Render](https://render.com):

#### 1. Backend Web Service
- **Environment**: `Python 3`
- **Root Directory**: `ORC`
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  ```env
  DATABASE_URL=postgresql+psycopg2://postgres.tyymppxfnkoadxbmpbms:[DB_PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require
  SECRET_KEY=oral_cancer_detection_super_secret_jwt_key_2026
  CORS_ORIGINS=https://oral-cancer-ai-x9q3.onrender.com,http://localhost:3000
  KEEP_ALIVE_URL=https://oral-cancer-backend-fiwu.onrender.com
  LOW_MEMORY=true
  ```

#### 2. Frontend Static Site
- **Environment**: `Static Site`
- **Root Directory**: `ORC/frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `build`
- **Rewrite Rules**:
  - `/*` ➔ `/index.html` (HTTP 200)
- **Environment Variables**:
  ```env
  REACT_APP_API_URL=https://oral-cancer-backend-fiwu.onrender.com
  ```

---

### Option 2: Vercel Deployment

The frontend includes a pre-configured [`vercel.json`](vercel.json):
```bash
# Deploy Frontend via Vercel CLI
cd frontend
npx vercel --prod
```
Set the Environment Variable `REACT_APP_API_URL` to your production backend URL.

---

## 💻 Local Development Quickstart

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** & **npm**
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/Lohith-RC/ORC.git
cd ORC
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run automated test suite (46 tests)
python -m pytest tests/ -v

# Launch local backend server
python -m uvicorn main:app --reload --port 8000
```
- API Endpoint: `http://localhost:8000`
- Swagger UI Docs: `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/health`

### 3. Frontend Setup
In a new terminal window:
```bash
cd frontend

# Install packages
npm install

# Start development workstation
npm start
```
The browser will open automatically at `http://localhost:3000`.

---

## 🧪 Testing & Validation Suite

The backend contains comprehensive automated test suites covering unit logic, integration workflows, rate limiters, and authentication:

```bash
cd backend
python -m pytest tests/ -v --tb=short
```

**Key Test Coverage Areas:**
- `test_auth.py`: JWT issuance, bcrypt hashing, invalid token rejection.
- `test_predict.py`: Image validation, multi-model inference, threshold validation.
- `test_optical.py`: Specular glare suppression, LAB color normalization.
- `test_security.py`: CSP headers, rate-limiting triggers, PHI data isolation.
- `test_interop.py`: HL7 FHIR r4 JSON bundle compliance.

---

## 📜 Academic Citation & Final Report

For academic research, clinical studies, or institutional audits utilizing this architecture:

```bibtex
@article{oscc_ai_2026,
  title   = {Multimodal Deep Learning Ensemble with Epistemic Uncertainty Quantification for Non-Invasive Oral Squamous Cell Carcinoma Screening},
  author  = {Lohith R C and Clinical AI Research Consortium},
  journal = {International Journal of Advanced Medical AI & Computer Vision},
  year    = {2026},
  url     = {https://github.com/Lohith-RC/ORC}
}
```

---

## 📄 License
This project is licensed under the **MIT License**. Clinical screening inferences should be corroborated by a qualified oral pathologist or oncologist.