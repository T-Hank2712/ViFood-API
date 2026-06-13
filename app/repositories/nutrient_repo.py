from app.models.nutrient import Nutrient
from app.repositories.base_repo import BaseRepository
# from app.helpers.slug import generate_key


class NutrientRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)
        
    def _map_allergy(self, record) -> Nutrient:
        n = record["n"]

        return Nutrient(
            id=n.get("id"),
            name=n.get("name"),
            key=n.get("key")
        )

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
