"""
Base Response Models
Các schema response chuẩn cho toàn bộ API
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, Generic, TypeVar
from datetime import datetime


DataT = TypeVar('DataT')


class BaseResponse(BaseModel):
    """Base response model cho tất cả API responses"""
    success: bool = Field(..., description="Trạng thái thành công hay thất bại")
    message: str = Field(..., description="Thông báo cho người dùng")
    timestamp: datetime = Field(default_factory=datetime.now, description="Thời điểm response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Thao tác thành công",
                "timestamp": "2026-03-10T10:30:00.123456"
            }
        }


class SuccessResponse(BaseResponse, Generic[DataT]):
    """Response model cho các request thành công với data"""
    success: bool = Field(default=True)
    data: DataT = Field(..., description="Dữ liệu trả về")


class ErrorResponse(BaseResponse):
    """Response model cho các request thất bại"""
    success: bool = Field(default=False)
    error_code: Optional[str] = Field(None, description="Mã lỗi để xử lý ở client")
    details: Optional[Any] = Field(None, description="Chi tiết lỗi (chỉ hiện ở development)")


class HealthCheckResponse(BaseModel):
    """Response model cho health check endpoint"""
    status: str = Field(..., description="Trạng thái hệ thống")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(..., description="Phiên bản API")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-03-10T10:30:00.123456",
                "version": "1.0.0"
            }
        }
