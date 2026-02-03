# ==================== Admin/Tenant Routes ====================
# File: app/api/v1/routes/tenants.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_admin_user, PaginationParams
from app.schemas import (
    TenantCreate, TenantResponse,
    TenantConfigUpdate, TenantConfigResponse
)
from app.models import User, Tenant, TenantConfigs
from app.api.responses import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/tenants", tags=["Tenants (Admin Only)"])


@router.post("", response_model=ResponseModel[TenantResponse])
async def create_tenant(
    tenant_data: TenantCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create new tenant (Admin only)
    """
    existing_tenant = db.query(Tenant).filter(Tenant.name == tenant_data.name).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant name already exists")
    
    tenant = Tenant(**tenant_data.dict())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    # Create default tenant config
    config = TenantConfigs(tenant_id=tenant.id)
    db.add(config)
    db.commit()
    
    return ResponseModel(
        success=True,
        data=tenant,
        message="Tenant created successfully"
    )


@router.get("", response_model=PaginatedResponse[TenantResponse])
async def list_tenants(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all tenants (Admin only)
    """
    query = db.query(Tenant)
    total_items = query.count()
    
    tenants = query.offset(pagination.skip)\
        .limit(pagination.page_size)\
        .all()
    
    total_pages = (total_items + pagination.page_size - 1) // pagination.page_size
    
    return PaginatedResponse(
        success=True,
        data=tenants,
        message="Tenants retrieved successfully",
        page=pagination.page,
        page_size=pagination.page_size,
        total_items=total_items,
        total_pages=total_pages
    )


@router.put("/{tenant_id}/config", response_model=ResponseModel[TenantConfigResponse])
async def update_tenant_config(
    tenant_id: int,
    config_data: TenantConfigUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update tenant configuration (Admin only)
    """
    config = db.query(TenantConfigs).filter(TenantConfigs.tenant_id == tenant_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Tenant config not found")
    
    update_data = config_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.commit()
    db.refresh(config)
    
    return ResponseModel(
        success=True,
        data=config,
        message="Tenant configuration updated successfully"
    )
