"""Territory model — regions, communes, watersheds, protected areas.
Uses plain text geometry (WKT/GeoJSON string) for SQLite compatibility.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Territory(Base):
    __tablename__ = "territories"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type = Column(
        String(50), nullable=False, index=True
    )  # country, macrozone, region, province, commune, watershed, protected_area
    parent_id = Column(Integer, ForeignKey("territories.id"), nullable=True)
    # Store geometry as GeoJSON text for SQLite compatibility
    geom_geojson = Column(Text, nullable=True)
    area_ha = Column(Float, nullable=True)
    population = Column(Integer, nullable=True)
    is_sample = Column(Boolean, default=False)
    source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parent = relationship("Territory", remote_side=[id], backref="children")
    prioritization_scores = relationship("PrioritizationScore", back_populates="territory")
