"""
Upload Service
Business logic cho upload functionality
"""
from fastapi import UploadFile, HTTPException
from pathlib import Path
from datetime import datetime
import aiofiles

from app.core.config import settings
from app.models.upload import UploadedFileInfo, DeleteFileResponse
from app.utils.file_utils import (
    generate_unique_filename,
    get_file_size_kb,
    validate_file_extension,
    ensure_directory_exists,
    delete_file_safely
)


class UploadService:
    """Service xử lý upload files"""
    
    def __init__(self):
        """Khởi tạo service và đảm bảo upload directory tồn tại"""
        self.upload_dir = settings.upload_dir
        ensure_directory_exists(self.upload_dir)
    
    async def upload_image(self, file: UploadFile) -> UploadedFileInfo:
        """
        Upload hình ảnh
        
        Args:
            file: File upload từ request
            
        Returns:
            UploadedFileInfo: Thông tin file đã upload
            
        Raises:
            HTTPException: Nếu có lỗi trong quá trình upload
        """
        # Validate file
        if not file:
            raise HTTPException(status_code=400, detail="Không có file được tải lên")
        
        # Validate extension
        if not validate_file_extension(file.filename, settings.allowed_image_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"Định dạng file không được hỗ trợ. Chỉ chấp nhận: {', '.join(settings.allowed_image_extensions)}"
            )
        
        # Read file content
        contents = await file.read()
        file_size = len(contents)
        
        # Validate size
        if file_size > settings.max_file_size:
            max_size_mb = settings.max_file_size / (1024 * 1024)
            raise HTTPException(
                status_code=400,
                detail=f"File quá lớn. Kích thước tối đa: {max_size_mb}MB"
            )
        
        # Generate unique filename
        unique_filename = generate_unique_filename(file.filename)
        file_path = self.upload_dir / unique_filename
        
        # Save file
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(contents)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Lỗi khi lưu file: {str(e)}"
            )
        
        # Get file info
        upload_date = datetime.now()
        size_kb = get_file_size_kb(file_path)
        file_extension = Path(file.filename).suffix.lower()
        
        # Create file URL
        file_url = f"/uploads/{unique_filename}"
        
        # Return file info
        return UploadedFileInfo(
            url=file_url,
            filename=unique_filename,
            original_filename=file.filename,
            upload_date=upload_date,
            upload_timestamp=int(upload_date.timestamp()),
            size_kb=size_kb,
            size_bytes=file_size,
            content_type=file.content_type or "application/octet-stream",
            extension=file_extension
        )
    
    async def delete_file(self, filename: str) -> DeleteFileResponse:
        """
        Xóa file đã upload
        
        Args:
            filename: Tên file cần xóa
            
        Returns:
            DeleteFileResponse: Thông tin file đã xóa
            
        Raises:
            HTTPException: Nếu file không tồn tại
        """
        file_path = self.upload_dir / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File không tồn tại")
        
        # Delete file
        success = delete_file_safely(file_path)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Không thể xóa file"
            )
        
        return DeleteFileResponse(
            filename=filename,
            deleted_at=datetime.now()
        )
    
    def get_upload_config(self):
        """
        Lấy cấu hình upload để client có thể query
        
        Returns:
            Dict chứa config
        """
        return {
            "max_file_size_mb": round(settings.max_file_size / (1024 * 1024), 2),
            "allowed_extensions": list(settings.allowed_image_extensions),
            "upload_endpoint": f"{settings.api_prefix}/upload/image"
        }


# Singleton instance
upload_service = UploadService()
