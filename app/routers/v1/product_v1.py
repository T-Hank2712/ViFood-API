from fastapi import APIRouter, UploadFile, File

from app.services.v1.product_service_v1 import ProductServiceV1

from fastapi import Depends, File, UploadFile

from app.core.dependencies import get_current_user
from app.models.user import User


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
    

@router.post("/products/extract")
async def extract_product(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):

    return await product_service.extract_from_image(
        user_id=current_user["user_id"],
        image=file,
    )
