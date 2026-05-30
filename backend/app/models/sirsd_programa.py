"""SIRSD Program model — stores soil recovery projects details and geometries."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from app.db.base import Base

class SirsdPrograma(Base):
    __tablename__ = "sirsd_programas"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(100), index=True, nullable=True)
    sup_ha = Column(Float, nullable=True)
    temporada = Column(Integer, nullable=True)
    concurso = Column(Integer, nullable=True)
    tip_conc = Column(String(100), nullable=True)
    codreg = Column(String(50), nullable=True)
    codprov = Column(String(50), nullable=True)
    comuna = Column(String(100), nullable=True)
    codcom = Column(String(50), nullable=True)
    sup_predio = Column(Float, nullable=True)
    su_uso_agr = Column(Float, nullable=True)
    sup_potres = Column(Float, nullable=True)
    clase = Column(String(100), nullable=True)
    subclase = Column(String(100), nullable=True)
    unidad = Column(String(255), nullable=True)
    agrupacion = Column(String(255), nullable=True)
    localidad = Column(String(255), nullable=True)
    conservado = Column(String(255), nullable=True)
    nom_operad = Column(String(255), nullable=True)
    bon_total = Column(Float, nullable=True)
    macrozona = Column(String(100), nullable=True)
    admisible = Column(String(100), nullable=True)
    
    # Store geometry as GeoJSON text for SQLite compatibility
    geom_geojson = Column(Text, nullable=True)
    
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
