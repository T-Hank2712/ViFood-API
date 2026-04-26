from app.models.ingredient import Ingredient

from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect

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


class IngredientServiceV0:

    @staticmethod
    def get_all_ingredients(): return ingredients

    @staticmethod
    def get_ingredient_by_id(ingredient_id: int):
        return next((i for i in ingredients if i.id == ingredient_id), None)
    
    @staticmethod
    def create_ingredient(name: str, description: str | None = None, image: str | None = None,
                          effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        new_id = max(i.id for i in ingredients) + 1 if ingredients else 1
        new_ingredient = Ingredient(id=new_id, name=name, description=description, image=image, effects=effects, found_in=found_in)
        ingredients.append(new_ingredient)
        return new_ingredient
    
    @staticmethod
    def update_ingredient(ingredient_id: int, name: str, description: str | None = None, image: str | None = None,
                          effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        ingredient = IngredientServiceV0.get_ingredient_by_id(ingredient_id)
        if ingredient:
            ingredient.name = name
            ingredient.description = description
            ingredient.image = image
            ingredient.effects = effects
            ingredient.found_in = found_in
            return ingredient
        return None
    
    @staticmethod
    def delete_ingredient(ingredient_id: int):
        global ingredients
        ingredients = [i for i in ingredients if i.id != ingredient_id]
        return {"message": "Ingredient deleted successfully"}
