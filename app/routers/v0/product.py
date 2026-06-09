"""Product v0 routes"""
from fastapi import APIRouter, Depends
from app.models.product import ProductCreate
from app.services.v0.product_service import ProductServiceV0
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["Products V0"],
)

product_service_v0 = ProductServiceV0()


@router.get("/")
async def list_products(current_user=Depends(get_current_user)):
    return {
        "message": "Get products success",
        "data": product_service_v0.get_all(current_user["user_id"])
    }


@router.get("/by-date")
async def get_products_by_date(
    day: int,
    month: int,
    year: int,
    current_user=Depends(get_current_user)
):
    return {
        "message": "Get products by date success",
        "data": product_service_v0.get_products_by_date(
            user_id=current_user["user_id"],
            day=day,
            month=month,
            year=year
        )
    }


@router.get("/count")
async def count_products(current_user=Depends(get_current_user)):
    return {
        "message": "Count products success",
        "data": {
            "count": product_service_v0.count(current_user["user_id"])
        }
    }


@router.get("/count-by-date")
async def count_products_by_date(
    day: int,
    month: int,
    year: int,
    current_user=Depends(get_current_user)
):
    count = product_service_v0.count_by_date(
        user_id=current_user["user_id"],
        day=day,
        month=month,
        year=year
    )

    return {
        "message": "Count products by date success",
        "data": {
            "day": day,
            "month": month,
            "year": year,
            "count": count
        }
    }


@router.get("/{product_id:int}")
async def get_product_by_id_v0(
    product_id: int,
    current_user=Depends(get_current_user)
):
    return product_service_v0.get_by_id(
        product_id=product_id,
        user_id=current_user["user_id"]
    )


@router.post("/")
async def create_product(
    product: ProductCreate,
    current_user=Depends(get_current_user)
):
    return product_service_v0.create_product(
        user_id=current_user["user_id"],
        product=product
    )
