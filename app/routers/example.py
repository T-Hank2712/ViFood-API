"""
Example Router
Template cho các router khác trong tương lai
"""
from fastapi import APIRouter, HTTPException
from app.models.base import SuccessResponse


router = APIRouter(
    prefix="/example",
    tags=["Example"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    summary="Example endpoint",
    description="Đây là ví dụ cho endpoint, có thể tạo thêm các router khác tương tự"
)
async def get_example():
    """
    Example GET endpoint
    """
    return SuccessResponse(
        success=True,
        message="This is an example endpoint",
        data={
            "info": "Bạn có thể tạo thêm nhiều router khác tương tự như thế này",
            "steps": [
                "Tạo file router mới trong app/routers/",
                "Tạo model/schema tương ứng trong app/models/",
                "Tạo service logic trong app/services/ (nếu cần)",
                "Import và register router trong app/main.py"
            ]
        }
    )


@router.post(
    "/",
    summary="Example POST endpoint"
)
async def create_example():
    """
    Example POST endpoint
    """
    return SuccessResponse(
        success=True,
        message="Created successfully",
        data={"id": 1}
    )


# TODO: Các router khác có thể tạo:
# - /api/users - User management
# - /api/auth - Authentication
# - /api/products - Product management
# - /api/orders - Order management
# - etc.
