"""
Products Alias Router
Alias /api/products/{id} với cơ chế default + canary rollout.
"""
from typing import Optional

from fastapi import APIRouter, Header, Response

from app.core.config import settings
from app.core.versioning import choose_products_version
from app.models.product import ProductResponse
from app.services.v0.product_service import product_service_v0
from app.services.v1.product_service import product_service_v1


router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{id}",
    response_model=ProductResponse,
    summary="Lấy thông tin sản phẩm theo ID (alias)",
    description="Alias endpoint: switch version theo config, hỗ trợ canary rollout"
)
async def get_product_alias(
    id: int,
    response: Response,
    x_canary_key: Optional[str] = Header(default=None, alias="X-Canary-Key")
):
    canary_key = x_canary_key or f"product:{id}"

    selected_version = choose_products_version(
        default_version=settings.products_default_version,
        canary_enabled=settings.products_canary_enabled,
        canary_percent=settings.products_canary_percent,
        canary_target_version=settings.products_canary_target_version,
        key=canary_key,
    )
    response.headers["X-Products-Version"] = selected_version

    if selected_version == "v1":
        return await product_service_v1.get_by_id(product_id=id)

    return await product_service_v0.get_by_id(product_id=id)
