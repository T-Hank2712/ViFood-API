# """
# Products Router V1
# Version v1 để phát triển truy vấn DB, tách biệt với v0.
# """
# from fastapi import APIRouter

# from app.models.product import Product
# from app.services.v1.product_service import product_service_v1


# router = APIRouter(
#     prefix="/products",
#     tags=["Products V1"],
#     responses={404: {"description": "Not found"}},
# )


# @router.get(
#     "/{id}",
#     response_model=Product,
#     summary="[v1] Lấy thông tin sản phẩm theo ID",
#     description="Version v1 (chuẩn bị cho logic truy vấn DB)"
# )
# async def get_product_by_id_v1(id: int):
#     return await product_service_v1.get_by_id(product_id=id)
