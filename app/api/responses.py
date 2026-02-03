# ==================== Response Models ====================
# File: app/api/responses.py

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: str

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool
    data: List[T]
    message: str
    page: int
    page_size: int
    total_items: int
    total_pages: int
