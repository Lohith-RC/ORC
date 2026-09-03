# Product Requirements Document

## Product Summary

**Product:** Visionary Diagnostics / OralCancer AI  
**Category:** AI-assisted oral cancer screening web application  
**Current status:** Functional academic prototype  
**Primary purpose:** Help authenticated users submit an oral-cavity photograph, receive an AI screening result, review risk indicators, and retain a history of analyses.

The product is a screening and triage aid. It must not be presented as a definitive diagnosis or a substitute for biopsy, pathology, or specialist examination.

## Problem

Oral cancer outcomes improve when suspicious lesions are identified early, but specialist access and awareness can be limited. The product reduces the first-step friction by combining:

- Image-based binary classification: `cancer` or `non_cancer`
- An `uncertain` safety outcome when model variance is high
- Patient risk-factor scoring
- Image-quality feedback
- A downloadable client-side PDF report

## Target Users

| User | Need |
|---|---|
| General user or patient | Accessible preliminary screening and next-step guidance |
| Frontline healthcare worker | Rapid triage support before referral |
| Clinician or researcher | Reviewable screening history and model signals |
| Project administrator | Maintain application, model, database, and deployment |

## Goals

1. Let users securely create an account and sign in.
2. Accept a valid oral image and optional clinical risk factors.
3. Return a clear screening result with confidence, uncertainty, clinical risk, and image-quality status.
4. Preserve analysis metadata in the user's history.
5. Encourage specialist referral for cancer, uncertain, high-risk, or low-quality outcomes.
6. Clearly communicate that the output is not a medical diagnosis.

## Non-Goals

- Definitive cancer diagnosis
- Treatment recommendation
- Histopathology, DICOM, or 3D scan analysis
- Multi-class lesion diagnosis in the current version
- Real Grad-CAM explanation in the current version
- Storing the uploaded image in the backend
- Regulatory or HIPAA compliance certification

## Current Functional Requirements

### Authentication

- Users can register with username, password, full name, and email.
- Username length must be 3-50 characters.
- Password length must be at least 6 characters.
- Login accepts username, case-insensitive username, or email.
- Successful login returns a JWT bearer token valid for 60 minutes.
- Protected pages require a token stored in browser `localStorage`.

### Screening

- Only authenticated users can submit an image.
- Backend accepts JPEG, PNG, and WEBP up to 10 MB.
- Frontend picker currently advertises JPEG, JPG, and PNG.
- User can provide age, tobacco use, alcohol use, betel-nut use, and prior oral-lesion history.
- Backend returns:
  - Prediction
  - Confidence
  - Uncertainty
  - Clinical risk score and high-risk alert
  - Image-quality status
  - TTA and MC Dropout pass counts

### Profile And History

- User can view and update full name and email.
- User can view previous analysis metadata in newest-first order.
- History stores the submitted filename, but not the image content.

### Reporting

- User can download a PDF generated in the browser from the visible result panel.
- The report may include the locally held image preview and result information.

### Informational Pages

- Public pages: Home, About, Contact, Login, Register.
- Protected pages: Upload and Profile.
- Theme selection supports light and dark modes.

## Product Rules

| Signal | Current Rule |
|---|---|
| Uncertain result | Maximum MC Dropout variance is greater than `0.015` |
| Low-quality image | Laplacian variance is below `50.0` |
| High clinical risk | Clinical risk score is at least `0.60` |
| Clinical risk | Age 40-59: +0.15; age 60+: +0.30; tobacco: +0.35; alcohol: +0.20; betel nut: +0.30; prior lesions: +0.25; capped at 1.0 |

## Success Metrics

### Product Metrics

- Registration and login success rate
- Screening completion rate
- Median and p95 inference latency
- Percentage of uncertain and low-quality outcomes
- Report download rate
- Percentage of users who review analysis history

### Model Metrics

- Sensitivity/recall for the cancer class
- Specificity for the non-cancer class
- F1 score and ROC-AUC
- Calibration error
- Uncertainty referral accuracy
- External-dataset performance

No verified evaluation artifact is currently present in the repository, so numerical accuracy claims must be treated as unverified until reproducible metrics are added.

## Safety And Compliance Requirements

- Every result view and PDF must display a medical disclaimer.
- Cancer, uncertain, high-risk, and low-quality outcomes must recommend professional review.
- Marketing copy must not claim HIPAA compliance without an audit and operational controls.
- Simulated Grad-CAM must not be presented as a real model explanation.
- Sensitive patient data must be minimized, protected in transit, and governed by a retention policy.

## Known Product Gaps

- Frontend hard-codes `http://localhost:8000` instead of using environment configuration.
- JWT is stored in `localStorage`, increasing exposure to cross-site scripting.
- Contact form and forgot-password button have no backend workflow.
- Profile displays a hard-coded membership date.
- Medical advisor, dataset, accuracy, privacy, and compliance claims are not verified by repository evidence.
- The backend permits wildcard CORS.
- There is no admin workflow, consent capture, audit log, model version in history, or delete-account/data workflow.

## Roadmap

### Release 1: Prototype Reliability

- Align configuration, validation, CORS, tests, and documentation.
- Add prominent screening disclaimer and actionable referral guidance.
- Record model version and complete clinical input snapshot with each analysis.

### Release 2: Clinical Evaluation

- Add reproducible model evaluation artifacts.
- Implement real Grad-CAM or remove the heatmap.
- Add calibration and external validation.
- Introduce clinician-reviewed multi-class lesion labels.

### Release 3: Production Readiness

- Secure deployment, secrets management, observability, backups, migrations, consent, retention, and privacy controls.
- Conduct clinical, security, legal, and regulatory review before real-world use.

