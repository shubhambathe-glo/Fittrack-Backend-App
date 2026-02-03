from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class PersonalRecord(Base):
    __tablename__ = "personal_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exercise_name = Column(String, nullable=False, index=True)
    record_type = Column(String, nullable=False)  # max_weight, max_reps, fastest_time, longest_distance
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    achieved_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="personal_records")
