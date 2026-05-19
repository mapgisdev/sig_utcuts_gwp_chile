"""Evidence file model — uploaded documents and files."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from app.db.base import Base


class EvidenceFile(Base):
    __tablename__ = "evidence_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(500), nullable=False)
    original_name = Column(String(500), nullable=True)
    file_type = Column(String(50), nullable=True)  # pdf, image, geojson, csv, xlsx
    file_size = Column(Integer, nullable=True)
    file_path = Column(String(1000), nullable=True)
    entity_type = Column(String(50), nullable=True)  # project, intervention, mrv_observation
    entity_id = Column(Integer, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
