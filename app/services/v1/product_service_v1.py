import httpx
from fastapi import UploadFile

from app.core.config import settings
from app.models.product import Product


class ProductServiceV1:

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

    async def extract_from_image(self, image: UploadFile) -> dict:
        file_content = await image.read()

        files = {
            "file": (
                image.filename,
                file_content,
                image.content_type or "image/jpeg"
            )
        }

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                settings.ai_api_url,
                files=files
            )

        response.raise_for_status()
        result = response.json()

        if not result.get("success"):
            raise Exception("AI API extract failed")

        return result["data"]
