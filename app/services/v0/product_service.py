"""
Product Service V0
Trả dữ liệu mock mặc định cho production ổn định.
"""
from datetime import datetime
from typing import List
from app.models.product import ProductResponse, ProductNutrition


class ProductServiceV0:
    async def get_all(self) -> List[ProductResponse]:
        """Lấy danh sách tất cả products (mock data)"""
        return [
            ProductResponse(
                _id=1,
                product_name="Sữa ABC",
                age_range="1-3 tuổi",
                ingredients=["Sữa bột", "Đường", "Dầu thực vật"],
                additive=["Chất điều vị (INS 621)"],
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
            ),
            ProductResponse(
                _id=2,
                product_name="Sữa Vinamilk",
                age_range="3-6 tuổi",
                ingredients=["Sữa bột", "Canxi", "Vitamin D"],
                additive=["Chất bảo quản (INS 202)"],
                nutrition=ProductNutrition(
                    energy="500 kcal",
                    protein="14 g",
                    fat="20 g",
                    sugar="18 g"
                ),
                manufacturer="Công ty Vinamilk",
                mfg_date="2025-11-15",
                expiry_date="2027-11-15",
                net_weight="1000g",
                allergen="Sản phẩm có chứa sữa",
                warning="Bảo quản nơi thoáng mát",
                origin="Việt Nam",
                createdAt=datetime.fromisoformat("2026-03-01T10:00:00.955+00:00"),
                timeZone="Asia/Ho_Chi_Minh",
                createdAtLocal="2026-03-01 17:00:00"
            ),
        ]
    async def get_by_id(self, product_id: int) -> ProductResponse:
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
    # async def create_product(self, product_data: ProductResponse) -> ProductResponse:


product_service_v0 = ProductServiceV0()
