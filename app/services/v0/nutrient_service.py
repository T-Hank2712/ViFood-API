from app.models.nutrient import Nutrient

from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect

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


class NutrientServiceV0:

    @staticmethod
    def get_all_nutrients(): return nutrients

    @staticmethod
    def get_nutrient_by_id(nutrient_id: int):
        return next((n for n in nutrients if n.id == nutrient_id), None)
    
    @staticmethod
    def create_nutrient(name: str, description: str | None = None, image: str | None = None,
                        effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        new_id = max(n.id for n in nutrients) + 1 if nutrients else 1
        new_nutrient = Nutrient(id=new_id, name=name, description=description, image=image, effects=effects, found_in=found_in)
        nutrients.append(new_nutrient)
        return new_nutrient
    
    @staticmethod
    def update_nutrient(nutrient_id: int, name: str, description: str | None = None, image: str | None = None,
                        effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        nutrient = NutrientServiceV0.get_nutrient_by_id(nutrient_id)
        if nutrient:
            nutrient.name = name
            nutrient.description = description
            nutrient.image = image
            nutrient.effects = effects
            nutrient.found_in = found_in
            return nutrient
        return None
    
    @staticmethod
    def delete_nutrient(nutrient_id: int):
        global nutrients
        nutrients = [n for n in nutrients if n.id != nutrient_id]
        return {"message": "Nutrient deleted successfully"}
