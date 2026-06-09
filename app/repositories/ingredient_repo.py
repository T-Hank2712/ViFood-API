from app.models.ingredient import Ingredient


class IngredientRepository:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.ingredients

    def get_by_id(self, ingredient_id: int):
        return next((i for i in self.db.ingredients if i.id == ingredient_id), None)

    def create(self, ingredient: Ingredient):
        self.db.ingredients.append(ingredient)
        return ingredient

    def delete(self, ingredient_id: int):
        self.db.ingredients[:] = [i for i in self.db.ingredients if i.id != ingredient_id]
        return True
