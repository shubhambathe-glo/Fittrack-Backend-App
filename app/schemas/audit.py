from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

# ==================== Audit Log Schemas ====================

class AuditLogBase(BaseModel):
    action_type: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    user_id: Optional[int] = None


class AuditLogResponse(AuditLogBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)
