"""Investment model — financial flows linked to projects."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    funding_source = Column(String(255), nullable=True)
    funding_type = Column(String(100), nullable=True)  # public, private, international, mixed
    amount = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    amount_usd = Column(Float, nullable=True)
    year = Column(Integer, nullable=True)
    financial_instrument = Column(String(255), nullable=True)
    approved_amount = Column(Float, nullable=True)
    executed_amount = Column(Float, nullable=True)
    committed_amount = Column(Float, nullable=True)
    source_document = Column(String(500), nullable=True)
    data_quality = Column(String(50), default="demo")  # demo, low, medium, high, official
    is_sample = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="investments")
