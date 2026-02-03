from sqlalchemy import (
    Column, Integer, Boolean, ForeignKey, DateTime, Time
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    email_enabled = Column(Boolean, default=True)
    push_enabled = Column(Boolean, default=True)
    workout_reminders = Column(Boolean, default=True)
    goal_milestones = Column(Boolean, default=True)
    streak_alerts = Column(Boolean, default=True)
    quiet_hours_start = Column(Time)
    quiet_hours_end = Column(Time)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="notification_preference")
