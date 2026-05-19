"""Intervention model — physical actions linked to projects."""
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    intervention_type = Column(
        String(100), nullable=True
    )  # restoration, afforestation, conservation, native_forest_management, fire_prevention, degradation_reduction
    ndc_component = Column(String(255), nullable=True)
    hectares_estimated = Column(Float, nullable=True)
    hectares_verified = Column(Float, nullable=True)
    tco2e_estimated = Column(Float, nullable=True)
    tco2e_verified = Column(Float, nullable=True)
    beneficiaries_estimated = Column(Integer, nullable=True)
    beneficiaries_verified = Column(Integer, nullable=True)
    status = Column(String(50), default="planned")
    verification_status = Column(String(50), default="estimated")
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="interventions")
    geometries = relationship("InterventionGeometry", back_populates="intervention")
    mrv_observations = relationship("MRVObservation", back_populates="intervention")


class InterventionGeometry(Base):
    __tablename__ = "intervention_geometries"

    id = Column(Integer, primary_key=True, index=True)
    intervention_id = Column(Integer, ForeignKey("interventions.id"), nullable=False)
    geometry_type = Column(String(50), nullable=True)  # polygon, point, multipolygon
    territory_id = Column(Integer, ForeignKey("territories.id"), nullable=True)
    # Store geometry as GeoJSON text for SQLite compatibility
    geom_geojson = Column(Text, nullable=True)
    precision_level = Column(
        String(50), nullable=True
    )  # national, regional, communal, polygon, point, parcel
    source = Column(String(255), nullable=True)
    validated = Column(Boolean, default=False)
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    intervention = relationship("Intervention", back_populates="geometries")
