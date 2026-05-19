"""Kobo / XLSForm Ingestion models — staging tables and synchronization configurations."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from app.db.base import Base


class KoboConfig(Base):
    __tablename__ = "kobo_configs"

    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(String(100), nullable=False, unique=True, index=True)
    form_name = Column(String(255), nullable=False)
    kobo_asset_id = Column(String(255), nullable=True)
    kobo_url = Column(String(500), default="https://kf.kobotoolbox.org/api/v2/assets/")
    api_token = Column(String(500), nullable=True)
    target_model = Column(String(100), nullable=True)  # project, mechanism, investment, intervention, mrv_observation, etc.
    auto_sync = Column(Boolean, default=False)
    last_sync_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class KoboStagingRecord(Base):
    __tablename__ = "kobo_staging_records"

    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(String(100), nullable=False, index=True)
    kobo_uuid = Column(String(255), nullable=True, index=True)
    payload_json = Column(Text, nullable=False)  # JSON dump of the raw Kobo submission
    status = Column(
        String(50), default="pending"
    )  # pending, validated, imported, failed
    validation_errors = Column(Text, nullable=True)  # JSON dump of validation issue list
    imported_entity_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
