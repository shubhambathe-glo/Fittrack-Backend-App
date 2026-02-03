from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Float, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class CardioActivity(Base):
    __tablename__ = "cardio_activities"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False, index=True)
    activity_type = Column(String, nullable=False)  # run, cycle, row, swim, etc.
    distance_km = Column(Float)
    duration_minutes = Column(Integer)
    avg_pace_min_per_km = Column(Float)
    avg_heart_rate = Column(Integer)
    max_heart_rate = Column(Integer)
    calories_burned = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workout = relationship("Workout", back_populates="cardio_activities")
