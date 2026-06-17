from fastapi import APIRouter

from app.services.v1.product_service_v1 import ProductServiceV1


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

product_service = ProductServiceV1()


@router.post("", summary="Tạo sản phẩm")
def create_product():
    result = product_service.create()

    return {
        "message": "Create Product success",
        "data": result
    }
