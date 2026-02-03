from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserConsent(Base):
    __tablename__ = "user_consents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    consent_type = Column(String, nullable=False)  # data_processing, analytics, marketing, etc.
    granted = Column(Boolean, default=False, nullable=False)
    version = Column(String, nullable=False)  # Policy version
    granted_at = Column(DateTime(timezone=True))
    revoked_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="consents")
    