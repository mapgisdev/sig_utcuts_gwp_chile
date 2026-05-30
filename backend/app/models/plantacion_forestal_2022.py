"""Plantacion Forestal 2022 model — stores forest plantations 2022 details and geometries."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from app.db.base import Base

class PlantacionForestal2022(Base):
    __tablename__ = "plantaciones_forestales_2022"

    id = Column(Integer, primary_key=True, index=True)
    objectid = Column(Integer, nullable=True)
    especie = Column(Integer, nullable=True)
    especie_t = Column(String(255), nullable=True)
    apl = Column(String(100), nullable=True)
    sup_ha = Column(Float, nullable=True)
    codreg = Column(String(50), nullable=True)
    
    # Store geometry as GeoJSON text for SQLite compatibility
    geom_geojson = Column(Text, nullable=True)
    
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
