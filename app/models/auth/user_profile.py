from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Date, 
    Float, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    full_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)  # Male, Female, Other, Prefer not to say
    height_cm = Column(Float)
    unit_preference = Column(String, default="metric")  # metric or imperial
    timezone = Column(String, default="UTC")
    language = Column(String, default="en")
    preferences = Column(JSON)  # {theme, dashboard_widgets, etc.}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")
