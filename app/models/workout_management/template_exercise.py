from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Float, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class TemplateExercise(Base):
    __tablename__ = "template_exercises"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("workout_templates.id"), nullable=False, index=True)
    exercise_name = Column(String, nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight_kg = Column(Float)
    order_index = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    template = relationship("WorkoutTemplate", back_populates="exercises")
