from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Float, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class BodyMeasurement(Base):
    __tablename__ = "body_measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    metric_type = Column(String, nullable=False)  # weight, body_fat_pct, waist, hips, chest, etc.
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)  # kg, lb, cm, inches, %
    measured_at = Column(DateTime(timezone=True), nullable=False, index=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="measurements")
