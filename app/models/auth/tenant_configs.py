from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class TenantConfigs(Base):
    __tablename__ = "tenant_configs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, unique=True)
    branding = Column(JSON)  # {logo_url, primary_color, secondary_color, etc.}
    feature_flags = Column(JSON)  # {social_enabled, coaching_enabled, etc.}
    user_policies = Column(JSON)  # {max_storage_mb, max_users, etc.}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="config")
