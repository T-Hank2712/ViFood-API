from fastapi import APIRouter, UploadFile, File

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
    

@router.post("/products/extract")
async def extract_product(file: UploadFile = File(...)):
    service = ProductServiceV1()
    return await service.extract_from_image(file)
