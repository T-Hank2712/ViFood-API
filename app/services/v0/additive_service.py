from app.models.additive import Additive
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect

additives = [
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
]


class AdditiveServiceV0:
    
    @staticmethod
    def get_all_additives(): return additives

    @staticmethod
    def get_additive_by_id(additive_id: int):
        return next((a for a in additives if a.id == additive_id), None)
    
    @staticmethod
    def create_additive(name: str, description: str | None = None, code: str | None = None, image: str | None = None,
                        effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        new_id = max(a.id for a in additives) + 1 if additives else 1
        new_additive = Additive(id=new_id, name=name, code=code, description=description, image=image,
                                effects=effects or [], found_in=found_in or [])
        additives.append(new_additive)
        return new_additive
    
    @staticmethod
    def update_additive(additive_id: int, name: str, description: str | None = None, code: str | None = None, image: str | None = None,
                        effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        additive = AdditiveServiceV0.get_additive_by_id(additive_id)
        if additive:
            additive.name = name
            additive.description = description
            additive.code = code
            additive.image = image
            additive.effects = effects or []
            additive.found_in = found_in or []
            return additive
        return None
    
    @staticmethod
    def delete_additive(additive_id: int):
        global additives
        additives = [a for a in additives if a.id != additive_id]
        return {"message": "Additive deleted successfully"}
