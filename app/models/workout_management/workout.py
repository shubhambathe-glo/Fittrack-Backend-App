from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Text, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    workout_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    workout_type = Column(String, nullable=False)  # strength, cardio, flexibility, mixed
    duration_minutes = Column(Integer)
    notes = Column(Text)
    tags = Column(JSON)  # ["5x5", "HIIT", "Mobility"]
    status = Column(String, default="completed")  # planned, completed, skipped
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="workouts")
    strength_exercises = relationship("StrengthExercise", back_populates="workout", cascade="all, delete-orphan")
    cardio_activities = relationship("CardioActivity", back_populates="workout", cascade="all, delete-orphan")
    media = relationship("WorkoutMedia", back_populates="workout", cascade="all, delete-orphan")
