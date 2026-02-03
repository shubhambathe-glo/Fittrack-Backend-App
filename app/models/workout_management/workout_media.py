from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class WorkoutMedia(Base):
    __tablename__ = "workout_media"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False, index=True)
    media_type = Column(String, nullable=False)  # image, video
    blob_url = Column(String, nullable=False)
    thumbnail_url = Column(String)
    file_size_bytes = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workout = relationship("Workout", back_populates="media")
