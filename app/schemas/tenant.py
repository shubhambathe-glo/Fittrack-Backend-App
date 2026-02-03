from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from app.schemas import TenantType

class TenantBase(BaseModel):
    name: str
    type: TenantType

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[TenantType] = None

class TenantResponse(TenantBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

class TenantConfigBase(BaseModel):
    branding: Optional[Dict[str, Any]] = None
    feature_flags: Optional[Dict[str, Any]] = None
    user_policies: Optional[Dict[str, Any]] = None

class TenantConfigCreate(TenantConfigBase):
    tenant_id: int

class TenantConfigUpdate(TenantConfigBase):
    pass

class TenantConfigResponse(TenantConfigBase):
    id: int
    tenant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)
