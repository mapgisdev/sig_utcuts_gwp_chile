"""Data quality model — flags for information gaps."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text

from app.db.base import Base


class DataQualityFlag(Base):
    __tablename__ = "data_quality_flags"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)  # project, investment, intervention, territory
    entity_id = Column(Integer, nullable=False)
    flag_type = Column(
        String(50), nullable=False
    )  # missing_geometry, missing_amount, missing_source, missing_year, low_confidence, estimated_value, missing_physical_indicator, missing_climate_indicator, possible_duplicate
    severity = Column(String(20), default="warning")  # info, warning, error, critical
    description = Column(Text, nullable=True)
    resolved = Column(Boolean, default=False)
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
