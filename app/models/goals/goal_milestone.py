from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, Date, 
    Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class GoalMilestone(Base):
    __tablename__ = "goal_milestones"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False, index=True)
    milestone_name = Column(String, nullable=False)
    milestone_value = Column(Float, nullable=False)
    target_date = Column(Date)
    achieved = Column(Boolean, default=False)
    achieved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    goal = relationship("Goal", back_populates="milestones")
