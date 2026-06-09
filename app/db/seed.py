from app.db.memory import FakeDB

from app.models.product import Product, ProductNutrition
from app.models.ingredient import Ingredient
from app.models.additive import Additive
from app.models.nutrient import Nutrient
from app.models.health_effect import HealthEffect
from app.models.food_category import FoodCategory
from app.models.allergy import Allergy
from app.models.disease import Disease
from app.models.health_goal import HealthGoal
# user and user_profile not required in seed data


def seed(db: FakeDB):
    # =========================
    # PRODUCTS
    # =========================
    db.products.extend([
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
            createdAt="2026-06-08T05:27:07.241790Z",
            timeZone="Asia/Ho_Chi_Minh",
            createdAtLocal="2026-06-08T12:27:07.241790+07:00"
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
            createdAt="2026-06-09T01:15:22.241790Z",
            timeZone="Asia/Ho_Chi_Minh",
            createdAtLocal="2026-06-09T08:15:22.241790+07:00"
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
            createdAt="2026-06-09T11:42:55.241790Z",
            timeZone="Asia/Ho_Chi_Minh",
            createdAtLocal="2026-06-09T18:42:55.241790+07:00"
        ),
    ])

    # =========================
    # INGREDIENTS
    # =========================
    db.ingredients.extend([
        Ingredient(
            id=1,
            name="Gạo",
            description="Nguyên liệu chính để nấu cơm",
            image="https://example.com/images/rice.png",
            effects=[
                HealthEffect(id=1, title="Tăng hương vị"),
                HealthEffect(id=2, title="Nguy cơ tăng cholesterol nếu nhiều"),
            ],
            found_in=[
                FoodCategory(id=1, name="Thịt đỏ"),
                FoodCategory(id=2, name="Rau bina"),
                FoodCategory(id=3, name="Đậu"),
            ],
        ),
        Ingredient(
            id=2,
            name="Thịt gà",
            description="Nguyên liệu giàu protein",
            image="https://example.com/images/chicken.png",
            effects=[
                HealthEffect(id=3, title="Tăng hương vị"),
                HealthEffect(id=4, title="Nguy cơ tăng cholesterol nếu nhiều"),
            ],
            found_in=[
                FoodCategory(id=1, name="Thịt đỏ"),
                FoodCategory(id=2, name="Rau bina"),
                FoodCategory(id=3, name="Đậu"),
            ],
        ),
        Ingredient(
            id=3,
            name="Rau cải",
            description="Nguyên liệu giàu chất xơ",
            image="https://example.com/images/vegetables.png",
            effects=[
                HealthEffect(id=5, title="Tăng hương vị"),
                HealthEffect(id=6, title="Nguy cơ tăng cholesterol nếu nhiều"),
            ],
            found_in=[
                FoodCategory(id=1, name="Thịt đỏ"),
                FoodCategory(id=2, name="Rau bina"),
                FoodCategory(id=3, name="Đậu"),
            ],
        ),
    ])

    # =========================
    # ADDITIVES
    # =========================
    db.additives.extend([
        Additive(
            id=1,
            name="Curcumin",
            code="E100",
            description="Curcumin - chất tạo màu vàng tự nhiên",
            image="https://example.com/images/e100.png",
            effects=[
                HealthEffect(id=1, title="Tăng hương vị"),
                HealthEffect(id=2, title="Nguy cơ tăng cholesterol nếu nhiều")
            ],
            found_in=[
                FoodCategory(id=1, name="Thịt đỏ"),
                FoodCategory(id=2, name="Rau bina"),
                FoodCategory(id=3, name="Đậu")
            ]
        ),
        Additive(
            id=2,
            name="Sorbic Acid",
            code="E200",
            description="Sorbic Acid - chất bảo quản chống nấm mốc",
            image="https://example.com/images/e200.png",
            effects=[
                HealthEffect(id=2, title="Chất bảo quản")
            ],
            found_in=[
                FoodCategory(id=2, name="Snacks", description="Đồ ăn vặt")
            ]
        ),
        Additive(
            id=3,
            name="Ascorbic Acid",
            code="E300",
            description="Ascorbic Acid - Vitamin C, chất chống oxy hóa",
            image="https://example.com/images/e300.png",
            effects=[
                HealthEffect(id=3, title="Chất chống oxy hóa")
            ],
            found_in=[
                FoodCategory(id=3, name="Đồ uống có ga", description="Nước ngọt")
            ]
        )
    ])
    
    # =========================
    # ALLERGIES
    # =========================
    
    db.allergies.extend([
        Allergy(id=1, name="Sữa"),
        Allergy(id=2, name="Gluten"),
        Allergy(id=3, name="Đậu phộng")])
    
    # =========================
    # DISEASES
    # =========================
    
    db.diseases.extend([
        Disease(id=1, name="Bệnh tiểu đường"),
        Disease(id=2, name="Bệnh tim mạch"),
        Disease(id=3, name="Bệnh béo phì")])
    
    # =========================
    # HEALTH GOALS
    # =========================
    db.health_goals.extend([
        HealthGoal(id=1, name="Giảm cân"),
        HealthGoal(id=2, name="Tăng cơ"),
        HealthGoal(id=3, name="Duy trì sức khỏe"),
    ])

    # =========================
    # NUTRIENTS
    # =========================
    db.nutrients.extend([
        Nutrient(
            id=1,
            name="Protein",
            description="Chất đạm giúp xây dựng cơ bắp",
            image="https://example.com/images/protein.png",
            effects=[HealthEffect(id=1, title="Tăng hương vị"), HealthEffect(id=2, title="Nguy cơ tăng cholesterol nếu nhiều")],
            found_in=[FoodCategory(id=1, name="Thịt đỏ"), FoodCategory(id=2, name="Rau bina"), FoodCategory(id=3, name="Đậu")],
        ),
        Nutrient(
            id=2,
            name="Carbohydrate",
            description="Tinh bột cung cấp năng lượng",
            image="https://example.com/images/carbohydrate.png",
            effects=[HealthEffect(id=3, title="Tăng hương vị"), HealthEffect(id=4, title="Nguy cơ tăng cholesterol nếu nhiều")],
            found_in=[FoodCategory(id=1, name="Thịt đỏ"), FoodCategory(id=2, name="Rau bina"), FoodCategory(id=3, name="Đậu")],
        ),
        Nutrient(
            id=3,
            name="Fat",
            description="Chất béo hỗ trợ hấp thụ vitamin",
            image="https://example.com/images/fat.png",
            effects=[HealthEffect(id=5, title="Tăng hương vị"), HealthEffect(id=6, title="Nguy cơ tăng cholesterol nếu nhiều")],
            found_in=[FoodCategory(id=1, name="Thịt đỏ"), FoodCategory(id=2, name="Rau bina"), FoodCategory(id=3, name="Đậu")],
        ),
    ])
    
    # =========================
    # FOOD CATEGORIES
    # =========================
    
    db.food_categories.extend([
        FoodCategory(id=1, name="Trái cây"),
        FoodCategory(id=2, name="Rau củ"),
        FoodCategory(id=3, name="Ngũ cốc"),
    ])
    
    # =========================
    # HEALTH EFFECTS
    # =========================
    
    db.health_effects.extend([
        HealthEffect(id=1, title="Tăng cường hệ miễn dịch"),
        HealthEffect(id=2, title="Hỗ trợ tiêu hóa"),
        HealthEffect(id=3, title="Giảm nguy cơ mắc bệnh tim mạch"),
    ])
