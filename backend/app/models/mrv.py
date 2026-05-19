"""MRV models — indicators and observations for monitoring, reporting, verification."""
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Date
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class MRVIndicator(Base):
    __tablename__ = "mrv_indicators"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(
        String(50), nullable=False
    )  # financial, physical, climate, social, biodiversity, governance, data_quality
    unit = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    calculation_method = Column(Text, nullable=True)
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    observations = relationship("MRVObservation", back_populates="indicator")


class MRVObservation(Base):
    __tablename__ = "mrv_observations"

    id = Column(Integer, primary_key=True, index=True)
    intervention_id = Column(Integer, ForeignKey("interventions.id"), nullable=False)
    indicator_id = Column(Integer, ForeignKey("mrv_indicators.id"), nullable=False)
    estimated_value = Column(Float, nullable=True)
    verified_value = Column(Float, nullable=True)
    observation_date = Column(Date, nullable=True)
    verification_status = Column(
        String(50), default="estimated"
    )  # estimated, reported, under_review, verified, rejected, needs_evidence
    evidence_file_id = Column(Integer, ForeignKey("evidence_files.id"), nullable=True)
    notes = Column(Text, nullable=True)
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    intervention = relationship("Intervention", back_populates="mrv_observations")
    indicator = relationship("MRVIndicator", back_populates="observations")

