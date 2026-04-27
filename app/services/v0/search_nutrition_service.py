from app.models.DTOs.searchDTO import searchDTO
from app.models.additive import Additive
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect
from app.models.ingredient import Ingredient
from app.models.nutrient import Nutrient
import random

nutrients = [
    Nutrient(id=1, name="Protein", description="Chất đạm giúp xây dựng cơ bắp", image="https://example.com/images/protein.png",
             effects=[HealthEffect(id=1, title="Tăng hương vị"), HealthEffect(id=2, title="Nguy cơ tăng cholesterol nếu nhiều")],
             found_in=[FoodCategory(id=1, name="Thịt đỏ"), FoodCategory(id=2, name="Rau bina"), FoodCategory(id=3, name="Đậu")]),
    Nutrient(id=2, name="Carbohydrate", description="Tinh bột cung cấp năng lượng", image="https://example.com/images/carbohydrate.png",
             effects=[HealthEffect(id=3, title="Tăng hương vị"), HealthEffect(id=4, title="Nguy cơ tăng cholesterol nếu nhiều")],
             found_in=[FoodCategory(id=1, name="Thịt đỏ"), FoodCategory(id=2, name="Rau bina"), FoodCategory(id=3, name="Đậu")]),
    Nutrient(id=3, name="Fat", description="Chất béo hỗ trợ hấp thụ vitamin", image="https://example.com/images/fat.png",
             effects=[HealthEffect(id=5, title="Tăng hương vị"), HealthEffect(id=6, title="Nguy cơ tăng cholesterol nếu nhiều")],
             found_in=[FoodCategory(id=1, name="Thịt đỏ"), FoodCategory(id=2, name="Rau bina"), FoodCategory(id=3, name="Đậu")])]

ingredients = [
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
]

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


class SearchNutritionServiceV0:
    @staticmethod
    def map_nutrient(n: Nutrient) -> searchDTO:
        return searchDTO(
            id=f"nutrient-{n.id}",
            name=n.name,
            description=n.description,
            image=n.image,
            effects=n.effects,
            found_in=n.found_in,
            type="nutrient"
        )
    
    @staticmethod
    def map_ingredient(i: Ingredient) -> searchDTO:
        return searchDTO(
            id=f"ingredient-{i.id}",
            name=i.name,
            description=i.description,
            image=i.image,
            effects=i.effects,
            found_in=i.found_in,
            type="ingredient"
        )
    
    @staticmethod
    def map_additive(a: Additive) -> searchDTO:
        return searchDTO(
            id=f"additive-{a.id}",
            name=a.name,
            code=a.code,
            description=a.description,
            image=a.image,
            effects=a.effects,
            found_in=a.found_in,
            type="additive"
        )
    
    @staticmethod
    def get_all_nutrition() -> list[searchDTO]:
        results: list[searchDTO] = []

        results += [SearchNutritionServiceV0.map_nutrient(n) for n in nutrients]
        results += [SearchNutritionServiceV0.map_ingredient(i) for i in ingredients]
        results += [SearchNutritionServiceV0.map_additive(a) for a in additives]

        random.shuffle(results)  # Trộn kết quả để đa dạng hơn
        return results

    @staticmethod
    def get_nutrition_by_id(nutrition_id: str) -> searchDTO | None:
        prefix, id_str = nutrition_id.split("-")
        id_num = int(id_str)

        if prefix == "nutrient":
            for n in nutrients:
                if n.id == id_num:
                    return SearchNutritionServiceV0.map_nutrient(n)
        elif prefix == "ingredient":
            for i in ingredients:
                if i.id == id_num:
                    return SearchNutritionServiceV0.map_ingredient(i)
        elif prefix == "additive":
            for a in additives:
                if a.id == id_num:
                    return SearchNutritionServiceV0.map_additive(a)

        return None
