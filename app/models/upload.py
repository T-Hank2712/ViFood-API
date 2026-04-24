"""
Upload Models/Schemas
Pydantic models cho upload functionality
"""
from pydantic import BaseModel, Field
from datetime import datetime


class UploadedFileInfo(BaseModel):
    """Schema cho thông tin file đã upload"""
    url: str = Field(..., description="Đường dẫn truy cập file")
    filename: str = Field(..., description="Tên file đã lưu (unique)")
    original_filename: str = Field(..., description="Tên file gốc")
    upload_date: datetime = Field(..., description="Ngày giờ upload (ISO format)")
    upload_timestamp: int = Field(..., description="Unix timestamp")
    size_kb: float = Field(..., description="Kích thước file (KB)")
    size_bytes: int = Field(..., description="Kích thước file (bytes)")
    content_type: str = Field(..., description="MIME type của file")
    extension: str = Field(..., description="Phần mở rộng file")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "/uploads/20260310_103000_a1b2c3d4_image.jpg",
                "filename": "20260310_103000_a1b2c3d4_image.jpg",
                "original_filename": "image.jpg",
                "upload_date": "2026-03-10T10:30:00.123456",
                "upload_timestamp": 1773158400,
                "size_kb": 245.67,
                "size_bytes": 251579,
                "content_type": "image/jpeg",
                "extension": ".jpg"
            }
        }


class DeleteFileResponse(BaseModel):
    """Schema cho response khi xóa file"""
    filename: str = Field(..., description="Tên file đã xóa")
    deleted_at: datetime = Field(default_factory=datetime.now, description="Thời điểm xóa")

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "20260310_103000_a1b2c3d4_image.jpg",
                "deleted_at": "2026-03-10T10:35:00.123456"
            }
        }


class UploadConfig(BaseModel):
    """Schema cho cấu hình upload (để client query)"""
    max_file_size_mb: float = Field(..., description="Kích thước file tối đa (MB)")
    allowed_extensions: list[str] = Field(..., description="Các định dạng file được phép")
    upload_endpoint: str = Field(..., description="Endpoint để upload")

    class Config:
        json_schema_extra = {
            "example": {
                "max_file_size_mb": 10.0,
                "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
                "upload_endpoint": "/api/upload/image"
            }
        }
