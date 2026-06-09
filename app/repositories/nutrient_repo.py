from app.models.nutrient import Nutrient


class NutrientRepository:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.nutrients

    def get_by_id(self, nutrient_id: int):
        return next((n for n in self.db.nutrients if n.id == nutrient_id), None)

    def create(self, nutrient: Nutrient):
        self.db.nutrients.append(nutrient)
        return nutrient

    def delete(self, nutrient_id: int):
        self.db.nutrients[:] = [n for n in self.db.nutrients if n.id != nutrient_id]
        return True
