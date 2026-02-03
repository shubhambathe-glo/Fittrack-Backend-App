from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Float, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class StrengthExercise(Base):
    __tablename__ = "strength_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False, index=True)
    exercise_name = Column(String, nullable=False, index=True)
    sets = Column(Integer)
    reps = Column(Integer)
    weight_kg = Column(Float)
    rpe = Column(Integer)  # Rate of Perceived Exertion (1-10)
    notes = Column(Text)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workout = relationship("Workout", back_populates="strength_exercises")
