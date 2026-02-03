from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    action_type = Column(String, nullable=False, index=True)  # login, create, update, delete, export
    entity_type = Column(String)  # workout, goal, profile, etc.
    entity_id = Column(Integer)
    old_value = Column(JSON)
    new_value = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
