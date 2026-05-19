"""Prioritization models — multi-criteria scoring for territories."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class PrioritizationScore(Base):
    __tablename__ = "prioritization_scores"

    id = Column(Integer, primary_key=True, index=True)
    territory_id = Column(Integer, ForeignKey("territories.id"), nullable=False)
    scenario_name = Column(String(100), default="default")
    score_total = Column(Float, nullable=True)
    score_forest_restoration = Column(Float, nullable=True)
    score_climate_risk = Column(Float, nullable=True)
    score_degradation_loss = Column(Float, nullable=True)
    score_financial_gap = Column(Float, nullable=True)
    score_biodiversity = Column(Float, nullable=True)
    score_social_vulnerability = Column(Float, nullable=True)
    score_operational_feasibility = Column(Float, nullable=True)
    score_mechanism_alignment = Column(Float, nullable=True)
    priority_class = Column(String(20), nullable=True)  # muy_alta, alta, media, baja, muy_baja
    is_sample = Column(Boolean, default=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)

    territory = relationship("Territory", back_populates="prioritization_scores")
