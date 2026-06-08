import datetime

from app.models.product import Product, ProductNutrition

# =========================
# FAKE DATABASE
# =========================

fake_products_db: list[Product] = [
    Product(
        _id=101,
        user_id=1,
        product_name="Sữa Dinh Dưỡng ABC Gold",
        age_range="1-3 tuổi",
        ingredients=[
            "Sữa bột nguyên kem",
            "Đường lactose",
            "Dầu thực vật",
            "Khoáng chất",
            "Vitamin tổng hợp"
        ],
        additive=[
            "Chất ổn định (INS 471)",
            "Chất nhũ hóa (INS 322)"
        ],
        nutrition=ProductNutrition(
            energy="450 kcal",
            protein="12 g",
            fat="18 g",
            sugar="20 g"
        ),
        manufacturer="Công ty Sữa ABC Việt Nam",
        mfg_date="2025-12-31",
        expiry_date="2027-12-31",
        net_weight="900g",
        allergen="Có chứa sữa, có thể chứa đậu nành",
        warning="Không dùng cho trẻ dưới 1 tuổi khi không có chỉ định bác sĩ",
        origin="Việt Nam",
        createdAt="2026-03-02T13:16:00.955Z",
        timeZone="Asia/Ho_Chi_Minh",
        createdAtLocal="2026-03-02 20:16:00"
    ),

    Product(
        _id=102,
        user_id=1,
        product_name="Bột Ăn Dặm HiKid Chuối",
        age_range="6-24 tháng",
        ingredients=[
            "Bột gạo",
            "Chuối sấy nghiền",
            "Sữa bột",
            "Dầu cá hồi",
            "Vitamin D3"
        ],
        additive=[
            "Chất chống đông vón (INS 551)"
        ],
        nutrition=ProductNutrition(
            energy="380 kcal",
            protein="8 g",
            fat="10 g",
            sugar="15 g"
        ),
        manufacturer="HiKid Nutrition Co.",
        mfg_date="2025-10-15",
        expiry_date="2027-10-15",
        net_weight="500g",
        allergen="Có chứa sữa",
        warning="Không dùng cho trẻ dị ứng đạm sữa bò",
        origin="Việt Nam",
        createdAt="2026-03-02T13:16:00.955Z",
        timeZone="Asia/Ho_Chi_Minh",
        createdAtLocal="2026-03-02 20:16:00"
    ),

    Product(
        _id=103,
        user_id=1,
        product_name="Nước Uống Điện Giải VitaPlus",
        age_range="Trên 12 tuổi",
        ingredients=[
            "Nước tinh khiết",
            "Muối khoáng",
            "Kali",
            "Magie",
            "Glucose"
        ],
        additive=[],
        nutrition=ProductNutrition(
            energy="120 kcal",
            protein="0 g",
            fat="0 g",
            sugar="28 g"
        ),
        manufacturer="VitaPlus Beverage JSC",
        mfg_date="2026-01-10",
        expiry_date="2027-01-10",
        net_weight="500ml",
        allergen=None,
        warning="Không dùng quá 1 lít/ngày",
        origin="Việt Nam",
        createdAt="2026-03-02T13:16:00.955Z",
        timeZone="Asia/Ho_Chi_Minh",
        createdAtLocal="2026-03-02 20:16:00"
    )
]


class ProductRepository:
    
    def __init__(self):
        self.db = fake_products_db

    def get_all(self, user_id: int) -> list[Product]:
        return [
            product
            for product in self.db
            if product.user_id == user_id
        ]

    def get_by_id(self, product_id: int, user_id: int) -> Product | None:
        for product in self.db:
            if product.id == product_id and product.user_id == user_id:
                return product
        return None

    def count(self, user_id: int) -> int:
        return len([
            product
            for product in self.db
            if product.user_id == user_id
        ])
        
    def create(self, user_id: int, product: Product) -> Product:
        new_id = max([p.id for p in self.db], default=100) + 1

        new_product = Product(
            _id=new_id,
            user_id=user_id,
            product_name=product.product_name,
            age_range=product.age_range,
            ingredients=product.ingredients,
            additive=product.additive,
            nutrition=product.nutrition,
            manufacturer=product.manufacturer,
            mfg_date=product.mfg_date,
            expiry_date=product.expiry_date,
            net_weight=product.net_weight,
            allergen=product.allergen,
            warning=product.warning,
            origin=product.origin,
            createdAt=datetime.datetime.now(datetime.timezone.utc),
            timeZone="Asia/Ho_Chi_Minh",
            createdAtLocal=datetime.datetime.now(datetime.timezone.utc)
        )

        self.db.append(new_product)
        return new_product
