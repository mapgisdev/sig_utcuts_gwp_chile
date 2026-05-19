"""Mechanism model — financial mechanisms for UTCUTS."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Mechanism(Base):
    __tablename__ = "mechanisms"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(500), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    main_funding_source = Column(String(255), nullable=True)
    maturity_level = Column(String(50), nullable=True)  # concept, design, pilot, operational, scaling
    time_horizon = Column(String(50), nullable=True)  # short, medium, long
    ndc_alignment = Column(String(255), nullable=True)
    target_beneficiaries = Column(String(500), nullable=True)
    enabling_conditions = Column(Text, nullable=True)
    intervention_types = Column(String(500), nullable=True)
    status = Column(String(50), default="active")
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = relationship("Project", back_populates="mechanism")
