import logging
from sqlalchemy import inspect, text
from app.db.session import engine
from app.core.config import settings

logger = logging.getLogger("app.db.migrations")

def run_safe_migrations() -> None:
    """Idempotent schema evolution ensuring columns and indexes exist across SQLite and PostgreSQL."""
    inspector = inspect(engine)
    with engine.begin() as conn:
        # 1. users table migrations
        user_cols = {c["name"] for c in inspector.get_columns("users")}
        if "role" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(30) DEFAULT 'clinician'"))
            logger.info("Database migration: added 'role' column to users")
        if "is_active" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1"))
            logger.info("Database migration: added 'is_active' column to users")
        if "created_at" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
            logger.info("Database migration: added 'created_at' column to users")

        # 2. analyses table migrations
        analysis_cols = {c["name"] for c in inspector.get_columns("analyses")}
        if "uncertainty" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN uncertainty REAL"))
        if "risk_score" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN risk_score REAL"))
        if "image_quality_score" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN image_quality_score REAL"))
        if "tta_used" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN tta_used INTEGER DEFAULT 0"))
        if "patient_identifier" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN patient_identifier VARCHAR(64) DEFAULT 'ANON-001'"))
            logger.info("Database migration: added 'patient_identifier' column to analyses")
        if "triage_tier" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN triage_tier VARCHAR(64)"))
            logger.info("Database migration: added 'triage_tier' column to analyses")
        if "telemetry_data" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN telemetry_data TEXT"))
            logger.info("Database migration: added 'telemetry_data' column to analyses")
        if "biopsy_proven" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN biopsy_proven BOOLEAN DEFAULT FALSE"))
            logger.info("Database migration: added 'biopsy_proven' column to analyses")
        if "ground_truth_dx" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN ground_truth_dx VARCHAR(64)"))
            logger.info("Database migration: added 'ground_truth_dx' column to analyses")
        if "histology_grade" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN histology_grade VARCHAR(32)"))
            logger.info("Database migration: added 'histology_grade' column to analyses")
        if "clinician_feedback_notes" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN clinician_feedback_notes TEXT"))
            logger.info("Database migration: added 'clinician_feedback_notes' column to analyses")
        if "annotated_contour" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN annotated_contour TEXT"))
            logger.info("Database migration: added 'annotated_contour' column to analyses")
        if "verified_at" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN verified_at TIMESTAMP"))
            logger.info("Database migration: added 'verified_at' column to analyses")
        if "verified_by_user_id" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN verified_by_user_id INTEGER"))
            logger.info("Database migration: added 'verified_by_user_id' column to analyses")

        # 3. Composite performance index migration
        analysis_indexes = {idx["name"] for idx in inspector.get_indexes("analyses")}
        if "idx_analyses_user_timestamp" not in analysis_indexes:
            try:
                conn.execute(text("CREATE INDEX idx_analyses_user_timestamp ON analyses (user_id, timestamp)"))
                logger.info("Database migration: created composite index idx_analyses_user_timestamp")
            except Exception as e:
                logger.warning(f"Index migration note: {e}")
        if "idx_analyses_patient_site" not in analysis_indexes:
            try:
                conn.execute(text("CREATE INDEX idx_analyses_patient_site ON analyses (user_id, patient_identifier, lesion_site)"))
                logger.info("Database migration: created composite index idx_analyses_patient_site")
            except Exception as e:
                logger.warning(f"Index migration note: {e}")
        if "idx_analyses_telemetry_gin" not in analysis_indexes and "postgresql" in settings.DATABASE_URL:
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_analyses_telemetry_gin ON analyses USING gin (cast(telemetry_data as jsonb))"))
                logger.info("Database migration: created GIN index on telemetry_data JSONB")
            except Exception as e:
                logger.warning(f"GIN index migration note: {e}")
