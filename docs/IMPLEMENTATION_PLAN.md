# Implementation Plan

## Objective

Turn the current academic prototype into a reproducible, safer, testable screening application while preserving the existing user flow and deployed MergedNet model.

## Priority Scale

- **P0:** Required before any public or clinical-facing deployment
- **P1:** Required for a reliable pilot
- **P2:** Product and maintainability improvement
- **P3:** Research roadmap

## Phase 0: Establish A Verified Baseline

**Priority:** P0

- Create a clean `.gitignore` for `venv`, databases, generated results, caches, and frontend build output.
- Add complete pinned backend dependencies.
- Replace training-script hard-coded paths with configuration.
- Add a model checksum and document exact model architecture/class order.
- Generate reproducible test-set metrics and confusion matrix from the checked-in dataset.
- Resolve conflicts between README claims and implemented behavior.

**Exit criteria**

- A new developer can install dependencies, run API and frontend, and reproduce a model evaluation.
- Accuracy and dataset claims point to generated artifacts.

## Phase 1: Backend Reliability And Security

**Priority:** P0

- Split `main.py` into configuration, database, schemas, auth, inference, and routes.
- Make `SECRET_KEY` mandatory outside development.
- Replace wildcard CORS with configured frontend origins.
- Add Alembic migrations and remove ad hoc schema migration logic.
- Validate image dimensions, decoded pixel count, filename length, and MIME/content consistency.
- Add structured error handling and request identifiers.
- Add concurrency control around inference.
- Store model version and inference configuration with every result.
- Decide whether authentication should move to secure HTTP-only cookies.

**Exit criteria**

- API security tests pass.
- No insecure production fallback secrets or wildcard CORS.
- Schema changes are migration-controlled.

## Phase 2: Model Validation And Safety

**Priority:** P0

- Fix MC Dropout so only dropout modules are stochastic; batch normalization remains in evaluation mode.
- Evaluate TTA and MC Dropout impact separately.
- Calibrate confidence and validate the `0.015` uncertainty threshold.
- Validate the `50.0` blur threshold on representative devices.
- Add sensitivity, specificity, F1, ROC-AUC, calibration, and referral metrics.
- Test model on an external dataset.
- Add explicit medical disclaimer and referral logic.
- Remove simulated Grad-CAM or replace it with a real backend-generated explanation.

**Exit criteria**

- Model card documents data, limitations, metrics, thresholds, and intended use.
- Safety outcomes are supported by validation evidence.

## Phase 3: Frontend Product Hardening

**Priority:** P1

- Centralize API client and environment-based base URL.
- Add token-expiry handling and consistent unauthorized redirects.
- Match frontend accepted formats with backend formats, including WEBP if retained.
- Add client-side file-size validation while preserving backend enforcement.
- Replace hard-coded membership date with backend `created_at`.
- Implement or remove forgot-password and contact-form controls.
- Improve result guidance for cancer, uncertain, high-risk, and low-quality states.
- Add consent and privacy notice before screening.
- Ensure PDF includes disclaimer, timestamp, model version, and referral guidance.
- Audit accessibility, keyboard interaction, contrast, reduced motion, and mobile layout.

**Exit criteria**

- Core flows meet accessibility and responsive checks.
- No dead controls or hard-coded environment endpoints.

## Phase 4: Data Model And Governance

**Priority:** P1

- Add analysis clinical inputs, model version, raw predicted class, final status, quality status, and timestamps with timezone.
- Add database constraints and indexes.
- Define retention, deletion, export, and consent policy.
- Add user-driven account and history deletion.
- Add audit logs without storing unnecessary sensitive content.
- Decide whether images must remain ephemeral or be retained with explicit consent.

**Exit criteria**

- Data lifecycle is documented and enforceable.
- Users can exercise deletion/export rights where applicable.

## Phase 5: Automated Testing And CI

**Priority:** P1

- Backend unit tests:
  - Risk scoring boundaries
  - Password hashing and legacy verification
  - Image-quality computation
  - Prediction override rules
- Backend API tests:
  - Auth success/failure
  - Duplicate user/email
  - Token validation
  - File type/size/corruption
  - Profile and history isolation
- Frontend tests:
  - Protected routes
  - Form validation
  - Result states
  - History and profile update
- End-to-end test:
  - Register -> login -> upload -> result -> history -> logout
- CI gates:
  - Formatting/linting
  - Tests
  - Dependency and secret scanning
  - Frontend production build

**Exit criteria**

- CI is required for merge and covers core flows.

## Phase 6: Deployment And Operations

**Priority:** P1

- Containerize backend and create production frontend build.
- Deploy PostgreSQL and run migrations.
- Configure HTTPS, reverse proxy, secure headers, and origin allowlist.
- Add health, readiness, and model-readiness checks.
- Add metrics for latency, failures, uncertain outcomes, and resource usage.
- Create backup, restore, rollback, and incident procedures.
- Load test CPU and GPU deployment options.

**Exit criteria**

- Staging deployment passes operational, security, and recovery checks.

## Phase 7: Research Enhancements

**Priority:** P3

- Multi-class ordinal lesion classification
- Class imbalance handling and focal loss
- True Grad-CAM++ or Score-CAM
- Hybrid CNN/vision-transformer architecture
- Federated learning research
- On-device inference research

These items require new validated data and must not be mixed into the production pipeline without evaluation.

## Suggested Delivery Order

| Sprint | Focus |
|---|---|
| 1 | Reproducible setup, dependencies, metrics baseline |
| 2 | Backend configuration, security, migrations |
| 3 | Model uncertainty and quality-threshold validation |
| 4 | Frontend safety, configuration, accessibility |
| 5 | Data governance and complete automated tests |
| 6 | Staging deployment, monitoring, load testing |

## Definition Of Done

- Implementation matches documentation.
- Tests cover success, failure, authorization, and safety states.
- Model metrics and limitations are reproducible.
- User-facing claims are evidence-based.
- No known P0 issue remains open.

