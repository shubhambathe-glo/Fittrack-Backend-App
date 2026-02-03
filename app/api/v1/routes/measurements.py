# ==================== Body Measurements Routes ====================
# File: app/api/v1/routes/measurements.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.db.session import get_db
from app.api.deps import get_current_user, PaginationParams
from app.schemas.measurement import BodyMeasurementCreate, BodyMeasurementResponse
from app.models import User, BodyMeasurement
from app.api.responses import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/measurements", tags=["Body Measurements"])


@router.post("", response_model=ResponseModel[BodyMeasurementResponse])
async def create_measurement(
    measurement_data: BodyMeasurementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Record body measurement
    """
    if measurement_data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot create measurement for other users")
    
    measurement = BodyMeasurement(**measurement_data.dict())
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    
    return ResponseModel(
        success=True,
        data=measurement,
        message="Measurement recorded successfully"
    )


@router.get("", response_model=PaginatedResponse[BodyMeasurementResponse])
async def list_measurements(
    pagination: PaginationParams = Depends(),
    metric_type: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List body measurements with filters
    """
    query = db.query(BodyMeasurement).filter(BodyMeasurement.user_id == current_user.id)
    
    if metric_type:
        query = query.filter(BodyMeasurement.metric_type == metric_type)
    if from_date:
        query = query.filter(BodyMeasurement.measured_at >= from_date)
    if to_date:
        query = query.filter(BodyMeasurement.measured_at <= to_date)
    
    total_items = query.count()
    measurements = query.order_by(BodyMeasurement.measured_at.desc())\
        .offset(pagination.skip)\
        .limit(pagination.page_size)\
        .all()
    
    total_pages = (total_items + pagination.page_size - 1) // pagination.page_size
    
    return PaginatedResponse(
        success=True,
        data=measurements,
        message="Measurements retrieved successfully",
        page=pagination.page,
        page_size=pagination.page_size,
        total_items=total_items,
        total_pages=total_pages
    )
