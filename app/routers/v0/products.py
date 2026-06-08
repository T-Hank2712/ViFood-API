"""
Products Router V0
Base API trả dữ liệu mẫu product (không truy vấn DB).
"""
from fastapi import APIRouter, Depends

from app.models.product import ProductCreate
from app.services.v0.product_service import ProductServiceV0
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["Products V0"],
    responses={404: {"description": "Not found"}},
)

product_service_v0 = ProductServiceV0()


@router.get("/")
async def list_products(
    current_user=Depends(get_current_user)
):
    """Lấy danh sách products của user hiện tại"""
    products = product_service_v0.get_all(user_id=current_user["user_id"])
    return {
        "message": "Get products success",
        "data": products
    }


@router.get("/{product_id}")
async def get_product_by_id_v0(
    product_id: int,
    current_user=Depends(get_current_user)
):
    """Lấy chi tiết product theo ID (chỉ của user hiện tại)"""

    return product_service_v0.get_by_id(
        product_id=product_id,
        user_id=current_user["user_id"]
    )
    
    
@router.post("/")
async def create_product(
    product: ProductCreate,
    current_user=Depends(get_current_user)
):
    """Tạo mới product"""

    return product_service_v0.create_product(user_id=current_user["user_id"], product=product)
