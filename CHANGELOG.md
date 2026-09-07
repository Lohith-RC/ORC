# Changelog

All notable changes to the OSCC AI Oral Cancer Detection Platform are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-09-07

### Security
- **Strict CORS Origin Whitelisting**: Eliminated wildcard `*` CORS in production. Allowed origins are now strictly validated against `CORS_ORIGINS`.
- **Startup Config Validation**: Added `settings.validate()` to assert that default or weak JWT secrets are blocked with critical exceptions in production environments.
- **Enterprise Security Headers**: Added `Content-Security-Policy`, `Cache-Control: no-store` on sensitive PHI/diagnostic endpoints, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, and `Strict-Transport-Security`.
- **Repository Hygiene**: Hardened `.gitignore` to reject `cloudflared.exe`, binary models (`*.pth`), SQLite databases, and `.env` files. Added `.env.example` template.

### Performance & ML Optimization
- **Kernel Warmup**: Added `warmup_model()` in application lifespan to preheat PyTorch CUDA/CPU kernels and eliminate cold-start inference latency.
- **Inference Efficiency**: Transitioned Test-Time Augmentation (TTA) forward passes to `torch.inference_mode()`, eliminating autograd engine tracking overhead.
- **Database Modularity**: Extracted schema migration logic from `main.py` into dedicated `app.db.migrations`.

### Frontend Architecture
- **Centralized Authentication**: Introduced `AuthContext` and `useAuth` hook for clean state propagation across the application.
- **Lazy Code-Splitting**: Migrated top-level routes to `React.lazy()` with `Suspense` fallbacks, improving initial page load time and bundle splitting.
- **Modular Component Design**: Extracted `UncertaintyCaliper`, `RiskFactorToggle`, `OfflineSyncBanner`, and reusable UI components (`SectionHeader`, `ToggleSwitch`, `StatusBadge`).
- **Jest Test Suite**: Fixed ESM resolution for React Router v7 and added automated unit test coverage for frontend common components.

### Continuous Integration & Testing
- **CI Modernization**: Upgraded Node.js to 20 LTS in GitHub Actions CI, added backend test coverage tracking with `pytest-cov`, and pinned dependencies in `requirements.txt`.
- **Automated Security Tests**: Added `tests/test_cors_and_security.py` verifying CORS preflight handling, origin restrictions, and security headers.
