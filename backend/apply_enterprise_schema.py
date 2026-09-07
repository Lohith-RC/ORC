import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("ERROR: DATABASE_URL not found in .env")
    sys.exit(1)

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

print(f"Connecting to Supabase PostgreSQL at: {db_url.split('@')[-1]}...")
engine = create_engine(db_url, pool_pre_ping=True)

schema_ddl = """
-- 1. Enable Cryptographic Extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Idempotent Custom Types
DO $$ BEGIN
    CREATE TYPE user_role_enum AS ENUM ('sys_admin', 'clinical_director', 'pathologist', 'screener_clinician', 'researcher');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE screening_site_enum AS ENUM ('buccal_mucosa', 'lateral_tongue', 'dorsal_tongue', 'floor_of_mouth', 'hard_palate', 'soft_palate', 'gingiva', 'lip');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. Multi-Tenant Clinic Hierarchy
CREATE TABLE IF NOT EXISTS tenants_clinics (
    clinic_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_code VARCHAR(32) NOT NULL UNIQUE,
    facility_name VARCHAR(255) NOT NULL,
    jurisdiction_country VARCHAR(3) NOT NULL DEFAULT 'IND',
    timezone VARCHAR(64) NOT NULL DEFAULT 'UTC',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert default clinic if none exists
INSERT INTO tenants_clinics (clinic_code, facility_name, jurisdiction_country)
VALUES ('DEFAULT_ORAL_ONCOLOGY', 'National Oral Cancer Screening Center', 'IND')
ON CONFLICT (clinic_code) DO NOTHING;

-- 4. De-Identified Patient Master (HIPAA Safe Harbor)
CREATE TABLE IF NOT EXISTS patients (
    patient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_id UUID NOT NULL REFERENCES tenants_clinics(clinic_id) ON DELETE RESTRICT,
    pseudo_mrn VARCHAR(64) NOT NULL,
    birth_year SMALLINT NOT NULL CHECK (birth_year BETWEEN 1900 AND 2026),
    gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F', 'O', 'U')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_patient_clinic_mrn UNIQUE (clinic_id, pseudo_mrn)
);

-- 5. Clinical Encounters
CREATE TABLE IF NOT EXISTS clinical_encounters (
    encounter_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(patient_id) ON DELETE RESTRICT,
    clinician_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    encounter_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    chief_complaint TEXT,
    lesion_site screening_site_enum NOT NULL DEFAULT 'buccal_mucosa',
    lesion_duration_weeks INT CHECK (lesion_duration_weeks >= 0),
    clinical_triage_decision VARCHAR(32) NOT NULL DEFAULT 'ROUTINE_MONITORING'
);
CREATE INDEX IF NOT EXISTS idx_encounters_patient_date ON clinical_encounters(patient_id, encounter_timestamp DESC);

-- 6. Epidemiological Risk Stratification
CREATE TABLE IF NOT EXISTS patient_risk_factors (
    risk_factor_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    encounter_id UUID NOT NULL UNIQUE REFERENCES clinical_encounters(encounter_id) ON DELETE CASCADE,
    tobacco_use BOOLEAN NOT NULL DEFAULT FALSE,
    tobacco_pack_years NUMERIC(5,2) DEFAULT 0.0 CHECK (tobacco_pack_years >= 0),
    alcohol_use BOOLEAN NOT NULL DEFAULT FALSE,
    alcohol_units_per_week INT DEFAULT 0 CHECK (alcohol_units_per_week >= 0),
    betel_quid_use BOOLEAN NOT NULL DEFAULT FALSE,
    betel_quid_years INT DEFAULT 0 CHECK (betel_quid_years >= 0),
    prior_oral_dysplasia BOOLEAN NOT NULL DEFAULT FALSE,
    hpv_diagnosed BOOLEAN DEFAULT NULL,
    composite_risk_score REAL NOT NULL CHECK (composite_risk_score BETWEEN 0.0 AND 1.0)
);

-- 7. Imaging Assets & Hardware Telemetry
CREATE TABLE IF NOT EXISTS imaging_assets (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    encounter_id UUID NOT NULL REFERENCES clinical_encounters(encounter_id) ON DELETE CASCADE,
    storage_bucket VARCHAR(64) NOT NULL DEFAULT 'oral-specimens',
    storage_object_path VARCHAR(512) NOT NULL,
    sha256_checksum CHAR(64) NOT NULL,
    mime_type VARCHAR(32) NOT NULL DEFAULT 'image/jpeg',
    file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes > 0),
    image_width INT NOT NULL DEFAULT 224,
    image_height INT NOT NULL DEFAULT 224,
    laplacian_sharpness_score REAL NOT NULL DEFAULT 50.0,
    is_acceptable_quality BOOLEAN NOT NULL DEFAULT TRUE,
    capture_device_make VARCHAR(64) DEFAULT 'Standard Optical Sensor',
    capture_device_model VARCHAR(64) DEFAULT 'Clinical Camera',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_image_checksum UNIQUE (sha256_checksum)
);
CREATE INDEX IF NOT EXISTS idx_images_encounter ON imaging_assets(encounter_id);

-- 8. Deep Learning Inference & Epistemic Uncertainty
CREATE TABLE IF NOT EXISTS model_inference_runs (
    inference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    image_id UUID NOT NULL REFERENCES imaging_assets(image_id) ON DELETE CASCADE,
    model_version VARCHAR(32) NOT NULL DEFAULT 'MergedNet_v2.0_FP16',
    model_weights_sha256 CHAR(64) NOT NULL DEFAULT '22abf275edfa5d8b737ad1750d641c2b5a57c03b',
    raw_cancer_probability REAL NOT NULL CHECK (raw_cancer_probability BETWEEN 0.0 AND 1.0),
    raw_non_cancer_probability REAL NOT NULL CHECK (raw_non_cancer_probability BETWEEN 0.0 AND 1.0),
    epistemic_uncertainty_variance REAL NOT NULL CHECK (epistemic_uncertainty_variance >= 0.0),
    tta_variance REAL NOT NULL DEFAULT 0.0,
    final_classification VARCHAR(16) NOT NULL CHECK (final_classification IN ('cancer', 'non_cancer', 'uncertain')),
    latency_ms REAL NOT NULL DEFAULT 450.0,
    inference_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_inference_image ON model_inference_runs(image_id);
CREATE INDEX IF NOT EXISTS idx_inference_classification_date ON model_inference_runs(final_classification, inference_timestamp);

-- 9. Pathological Ground Truth (Biopsy Confirmation)
CREATE TABLE IF NOT EXISTS clinical_ground_truth (
    ground_truth_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    encounter_id UUID NOT NULL UNIQUE REFERENCES clinical_encounters(encounter_id) ON DELETE RESTRICT,
    biopsy_confirmed BOOLEAN NOT NULL DEFAULT TRUE,
    histological_grade VARCHAR(32) CHECK (histological_grade IN ('hyperplasia', 'mild_dysplasia', 'mod_dysplasia', 'severe_dysplasia', 'oscc_stage_i', 'oscc_stage_ii', 'oscc_stage_iii', 'oscc_stage_iv')),
    pathologist_id INTEGER NOT NULL REFERENCES users(id),
    verification_date DATE NOT NULL DEFAULT CURRENT_DATE,
    pathology_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 10. Real-Time Clinician Dashboard Materialized View
DROP MATERIALIZED VIEW IF EXISTS mv_clinician_patient_dashboard;
CREATE MATERIALIZED VIEW mv_clinician_patient_dashboard AS
SELECT 
    e.encounter_id,
    e.encounter_timestamp,
    p.patient_id,
    p.pseudo_mrn,
    p.gender,
    (EXTRACT(YEAR FROM CURRENT_DATE) - p.birth_year) AS calculated_age,
    e.lesion_site,
    e.clinical_triage_decision,
    r.composite_risk_score,
    r.tobacco_use,
    r.betel_quid_use,
    m.final_classification AS ai_prediction,
    m.raw_cancer_probability AS ai_confidence,
    m.epistemic_uncertainty_variance AS ai_uncertainty,
    gt.histological_grade AS biopsy_outcome
FROM clinical_encounters e
JOIN patients p ON e.patient_id = p.patient_id
LEFT JOIN patient_risk_factors r ON e.encounter_id = r.encounter_id
LEFT JOIN imaging_assets img ON e.encounter_id = img.encounter_id
LEFT JOIN model_inference_runs m ON img.image_id = m.image_id
LEFT JOIN clinical_ground_truth gt ON e.encounter_id = gt.encounter_id;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_dashboard_encounter ON mv_clinician_patient_dashboard(encounter_id);
"""

print("Executing Enterprise Data Modeling DDL in Supabase...")
raw_conn = engine.raw_connection()
try:
    cursor = raw_conn.cursor()
    cursor.execute(schema_ddl)
    raw_conn.commit()
    cursor.close()
    print("SUCCESS: All enterprise schemas, tables, indexes, and materialized views applied to Supabase PostgreSQL!")
finally:
    raw_conn.close()

# Inspect and print all tables in public schema
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()

with engine.connect() as conn:
    mv_res = conn.execute(text("SELECT matviewname FROM pg_matviews WHERE schemaname = 'public';")).fetchall()
    mat_views = [r[0] for r in mv_res]

print("\nCurrent Tables in Supabase public schema:")
for t in tables:
    print(f"  - Table: {t}")

print("\nMaterialized Views in Supabase public schema:")
for mv in mat_views:
    print(f"  - Materialized View: {mv}")

