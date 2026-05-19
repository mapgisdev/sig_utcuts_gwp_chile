"""Project model — UTCUTS projects linked to mechanisms."""
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Table
)
from sqlalchemy.orm import relationship

from app.db.base import Base

# Many-to-many: projects <-> territories
project_territories = Table(
    "project_territories",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("territory_id", Integer, ForeignKey("territories.id"), primary_key=True),
)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    mechanism_id = Column(Integer, ForeignKey("mechanisms.id"), nullable=True)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    status = Column(String(50), default="draft")  # draft, active, completed, cancelled
    geographic_precision = Column(
        String(50), nullable=True
    )  # national, regional, communal, polygon, point, parcel
    data_confidence = Column(String(50), default="demo")  # demo, low, medium, high, official
    source_reference = Column(String(500), nullable=True)
    is_sample = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mechanism = relationship("Mechanism", back_populates="projects")
    investments = relationship("Investment", back_populates="project")
    interventions = relationship("Intervention", back_populates="project")
    territories = relationship("Territory", secondary=project_territories)
