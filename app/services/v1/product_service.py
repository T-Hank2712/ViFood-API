"""
Product Service V1
Nơi triển khai truy vấn DB cho version v1.
"""
from datetime import datetime

from app.models.product import ProductNutrition, ProductResponse


class ProductServiceV1:
    async def get_by_id(self, product_id: int) -> ProductResponse:
        """
        TODO (v1):
        - Query database theo product_id
        - Map dữ liệu DB sang ProductResponse
        - Nếu không tìm thấy thì raise HTTPException(404)

        Tạm thời trả mock để endpoint v1 chạy ổn trong lúc phát triển.
        """
        return ProductResponse(
            _id=product_id,
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
            nutrition=ProductNutrition(
                energy="450 kcal",
                protein="12 g",
                fat="18 g",
                sugar="20 g"
            ),
            manufacturer="Công ty XYZ",
            mfg_date="2025-12-31",
            expiry_date="2027-12-31",
            net_weight="900g",
            allergen="Sản phẩm có chứa sữa",
            warning="Không sử dụng cho trẻ em dưới 3 tuổi",
            origin="Việt Nam",
            createdAt=datetime.fromisoformat("2026-03-02T13:16:00.955+00:00"),
            timeZone="Asia/Ho_Chi_Minh",
            createdAtLocal="2026-03-02 20:16:00"
        )


product_service_v1 = ProductServiceV1()
