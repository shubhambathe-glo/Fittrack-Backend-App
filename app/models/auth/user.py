from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    workouts = relationship("Workout", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    measurements = relationship("BodyMeasurement", back_populates="user")
    notification_preference = relationship("NotificationPreference", back_populates="user", uselist=False)
    consents = relationship("UserConsent", back_populates="user")
    templates = relationship("WorkoutTemplate", back_populates="user")
    personal_records = relationship("PersonalRecord", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
