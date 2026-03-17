"""
Upload Router
API endpoints cho upload functionality
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.models.base import SuccessResponse
from app.models.upload import UploadedFileInfo, DeleteFileResponse, UploadConfig
from app.services.upload_service import upload_service
from app.core.dependencies import verify_api_key


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/config",
    response_model=UploadConfig,
    summary="Lấy cấu hình upload",
    description="Trả về các thông số cấu hình upload để client sử dụng"
)
async def get_upload_config():
    """
    Lấy cấu hình upload (max size, allowed extensions, etc.)
    """
    config = upload_service.get_upload_config()
    return config


@router.post(
    "/image",
    response_model=SuccessResponse[UploadedFileInfo],
    status_code=200,
    summary="Upload hình ảnh",
    description="Upload một file hình ảnh và nhận về thông tin file (yêu cầu API Key)"
)
async def upload_image(
    file: UploadFile = File(..., description="File hình ảnh cần upload"),
    api_key: str = Depends(verify_api_key)
):
    """
    Upload hình ảnh
    
    - **file**: File hình ảnh (jpg, jpeg, png, gif, webp, bmp)
    - **max_size**: 10MB
    
    Returns:
        - url: Đường dẫn truy cập ảnh
        - filename: Tên file đã lưu (unique)
        - original_filename: Tên file gốc
        - upload_date: Ngày giờ tải lên (ISO format)
        - upload_timestamp: Unix timestamp
        - size_kb: Kích thước file (KB)
        - size_bytes: Kích thước file (bytes)
        - content_type: MIME type
        - extension: Phần mở rộng file
    """
    try:
        file_info = await upload_service.upload_image(file)
        
        return SuccessResponse(
            success=True,
            message="Upload thành công",
            data=file_info
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi không xác định: {str(e)}"
        )


@router.delete(
    "/image/{filename}",
    response_model=SuccessResponse[DeleteFileResponse],
    summary="Xóa hình ảnh",
    description="Xóa một file hình ảnh đã upload (yêu cầu API Key)"
)
async def delete_image(
    filename: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Xóa hình ảnh đã upload
    
    - **filename**: Tên file cần xóa (lấy từ response của upload)
    """
    try:
        delete_info = await upload_service.delete_file(filename)
        
        return SuccessResponse(
            success=True,
            message="Xóa file thành công",
            data=delete_info
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi không xác định: {str(e)}"
        )


# TODO: Có thể thêm các endpoint khác như:
# - Upload multiple files
# - Get file info by filename
# - List uploaded files (với pagination)
# - Upload file types khác (PDF, documents, etc.)
