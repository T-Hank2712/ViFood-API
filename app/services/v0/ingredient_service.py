from app.models.ingredient import Ingredient

ingredients = [
    Ingredient(id=1, name="Gạo", description="Nguyên liệu chính để nấu cơm"),
    Ingredient(id=2, name="Thịt gà", description="Nguyên liệu giàu protein"),
    Ingredient(id=3, name="Rau cải", description="Nguyên liệu giàu chất xơ")]


class IngredientServiceV0:

    @staticmethod
    def get_all_ingredients(): return ingredients

    @staticmethod
    def get_ingredient_by_id(ingredient_id: int):
        return next((i for i in ingredients if i.id == ingredient_id), None)
    
    @staticmethod
    def create_ingredient(name: str, description: str | None = None):
        new_id = max(i.id for i in ingredients) + 1 if ingredients else 1
        new_ingredient = Ingredient(id=new_id, name=name, description=description)
        ingredients.append(new_ingredient)
        return new_ingredient
    
    @staticmethod
    def update_ingredient(ingredient_id: int, name: str, description: str | None = None):
        ingredient = IngredientServiceV0.get_ingredient_by_id(ingredient_id)
        if ingredient:
            ingredient.name = name
            ingredient.description = description
            return ingredient
        return None
    
    @staticmethod
    def delete_ingredient(ingredient_id: int):
        global ingredients
        ingredients = [i for i in ingredients if i.id != ingredient_id]
        return {"message": "Ingredient deleted successfully"}
