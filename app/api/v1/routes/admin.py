# File: app/api/v1/routes/admin.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.api.deps import get_current_admin_user, PaginationParams
from app.schemas import UserResponse, UserDetailResponse
from app.models import User, Tenant, UserProfile
from app.api.responses import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/admin", tags=["Admin - User Management"])


# ==================== User Management (Admin) ====================

@router.get("/users", response_model=PaginatedResponse[UserDetailResponse])
async def list_all_users(
    pagination: PaginationParams = Depends(),
    tenant_id: Optional[int] = Query(None, description="Filter by tenant ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_admin: Optional[bool] = Query(None, description="Filter by admin status"),
    search: Optional[str] = Query(None, description="Search by email or name"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get all users in the system with filters (Admin only)
    
    Filters:
    - tenant_id: Filter by specific tenant
    - is_active: Filter active/inactive users
    - is_admin: Filter admin/regular users
    - search: Search by email or profile name
    """
    query = db.query(User)
    
    # Apply filters
    if tenant_id is not None:
        query = query.filter(User.tenant_id == tenant_id)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)
    
    if search:
        # Join with UserProfile to search by name
        query = query.outerjoin(UserProfile).filter(
            (User.email.ilike(f"%{search}%")) | 
            (UserProfile.full_name.ilike(f"%{search}%"))
        )
    
    # Get total count
    total_items = query.count()
    
    # Apply pagination and ordering
    users = query.order_by(User.created_at.desc())\
        .offset(pagination.skip)\
        .limit(pagination.page_size)\
        .all()
    
    total_pages = (total_items + pagination.page_size - 1) // pagination.page_size
    
    return PaginatedResponse(
        success=True,
        data=users,
        message="Users retrieved successfully",
        page=pagination.page,
        page_size=pagination.page_size,
        total_items=total_items,
        total_pages=total_pages
    )


@router.get("/users/{user_id}", response_model=ResponseModel[UserDetailResponse])
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get specific user details by ID (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return ResponseModel(
        success=True,
        data=user,
        message="User retrieved successfully"
    )


@router.patch("/users/{user_id}/activate", response_model=ResponseModel[UserResponse])
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Activate a user account (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    db.refresh(user)
    
    return ResponseModel(
        success=True,
        data=user,
        message="User activated successfully"
    )


@router.patch("/users/{user_id}/deactivate", response_model=ResponseModel[UserResponse])
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Deactivate a user account (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deactivating themselves
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    
    user.is_active = False
    db.commit()
    db.refresh(user)
    
    return ResponseModel(
        success=True,
        data=user,
        message="User deactivated successfully"
    )


@router.delete("/users/{user_id}", response_model=ResponseModel[None])
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Permanently delete a user (Admin only)
    
    WARNING: This will cascade delete all user data (workouts, goals, etc.)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    db.delete(user)
    db.commit()
    
    return ResponseModel(
        success=True,
        data=None,
        message="User deleted successfully"
    )


@router.get("/users/stats/summary", response_model=ResponseModel[dict])
async def get_users_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get user statistics summary (Admin only)
    """
    from sqlalchemy import func
    
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    inactive_users = total_users - active_users
    admin_users = db.query(User).filter(User.is_admin == True).count()
    
    # Users per tenant
    users_per_tenant = db.query(
        Tenant.name,
        Tenant.type,
        func.count(User.id).label('user_count')
    ).join(User).group_by(Tenant.id).all()
    
    tenant_stats = [
        {
            "tenant_name": name,
            "tenant_type": type_,
            "user_count": count
        }
        for name, type_, count in users_per_tenant
    ]
    
    stats = {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "admin_users": admin_users,
        "regular_users": total_users - admin_users,
        "users_per_tenant": tenant_stats
    }
    
    return ResponseModel(
        success=True,
        data=stats,
        message="User statistics retrieved successfully"
    )
