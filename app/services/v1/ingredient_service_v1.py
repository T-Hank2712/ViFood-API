from app.repositories.ingredient_repo import IngredientRepository


class IngredientServiceV1:

    def __init__(self, db):
        self.repo = IngredientRepository(db)

    def get_all_ingredients(self):
        ingredients = self.repo.get_all()

        if not ingredients:
            raise ValueError("Ingredient Not Found")

        return ingredients

    def get_ingredient_by_id(self, ingredient_id: str):
        ingredient = self.repo.get_by_id(ingredient_id)

        if not ingredient:
            raise ValueError("Ingredient Not Found")

        return ingredient
