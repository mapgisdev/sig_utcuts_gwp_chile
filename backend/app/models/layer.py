"""Layer and DataSource models — geospatial layers and their sources."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    url = Column(String(500), nullable=True)
    access_type = Column(String(50), nullable=True)  # open, restricted, api, wms
    update_frequency = Column(String(100), nullable=True)
    license = Column(String(255), nullable=True)
    spatial_resolution = Column(String(100), nullable=True)
    temporal_resolution = Column(String(100), nullable=True)
    geometry_type = Column(String(50), nullable=True)
    integration_status = Column(
        String(50), default="planned"
    )  # planned, manual_download, semi_automated, automated_api, wms_wfs, deprecated, unavailable
    notes = Column(Text, nullable=True)
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    layers = relationship("Layer", back_populates="data_source")


class Layer(Base):
    __tablename__ = "layers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # territorial, forest, climate, biodiversity, financial, prioritization
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=True)
    source_url = Column(String(500), nullable=True)
    layer_type = Column(String(50), default="geojson")  # geojson, wms, wfs, tiles
    geometry_type = Column(String(50), nullable=True)
    style_config = Column(Text, nullable=True)  # JSON config for MapLibre styling
    is_active = Column(Boolean, default=True)
    is_official = Column(Boolean, default=False)
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    data_source = relationship("DataSource", back_populates="layers")
