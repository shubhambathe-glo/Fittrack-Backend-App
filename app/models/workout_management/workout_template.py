from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, Text, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class WorkoutTemplate(Base):
    __tablename__ = "workout_templates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    template_name = Column(String, nullable=False)
    workout_type = Column(String, nullable=False)
    description = Column(Text)
    tags = Column(JSON)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="templates")
    exercises = relationship("TemplateExercise", back_populates="template", cascade="all, delete-orphan")
