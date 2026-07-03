import httpx
from fastapi import UploadFile

from app.core.config import settings
from app.models.product import Product
from app.services.s3_service import S3Service


class ProductServiceV1:
    def __init__(self):
        self.s3_service = S3Service(settings)

    def create(self) -> Product:
        return Product(
            product_name="Sữa ABC",
            age_range="1-3 tuổi",
            ingredients=[
                "Sữa bột",
                "Đường",
                "Dầu thực vật"
            ],
            additive=[
                "Chất điều vị (INS 621)"
            ],
            nutrition={
                "energy": "450 kcal",
                "protein": "12 g",
                "fat": "18 g",
                "sugar": "20 g"
            },
            manufacturer="Công ty XYZ",
            mfg_date="2025-12-31",
            expiry_date="2027-12-31",
            net_weight="900g",
            allergen="Sản phẩm có chứa sữa",
            warning="Không sử dụng cho trẻ em dưới 3 tuổi",
            origin="Việt Nam"
        )

    async def extract_from_image(self, user_id: str, image: UploadFile) -> dict:
        file_content = await image.read()
        content_type = image.content_type or "image/jpeg"

        s3_key = self.s3_service.upload_file(
            user_id=user_id,
            file_content=file_content,
            content_type=content_type,
        )

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                settings.ai_api_url,
                json={
                    "s3_key": s3_key,
                },
            )

        response.raise_for_status()
        result = response.json()

        if not result.get("success"):
            raise Exception("AI API extract failed")
        
        return {
            "s3_key": s3_key,
            "data": result["data"],
        }
