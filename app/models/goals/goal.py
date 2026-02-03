from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Date, 
    Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    goal_name = Column(String, nullable=False)
    metric_type = Column(String, nullable=False)  # weight, distance, workout_count, exercise_1rm, etc.
    target_value = Column(Float, nullable=False)
    baseline_value = Column(Float)
    unit = Column(String)  # kg, km, count, minutes
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(String, default="active")  # active, completed, abandoned
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="goals")
    milestones = relationship("GoalMilestone", back_populates="goal", cascade="all, delete-orphan")
