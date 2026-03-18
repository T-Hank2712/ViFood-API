"""
Products Router V0
Base API trả dữ liệu mẫu product (không truy vấn DB).
"""
from fastapi import APIRouter

from app.models.product import ProductResponse
from app.services.v0.product_service import product_service_v0


router = APIRouter(
    prefix="/products",
    tags=["Products V0"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{id}",
    response_model=ProductResponse,
    summary="[v0] Lấy thông tin sản phẩm theo ID",
    description="Version v0 trả dữ liệu mẫu mặc định"
)
async def get_product_by_id_v0(id: int):
    return await product_service_v0.get_by_id(product_id=id)
