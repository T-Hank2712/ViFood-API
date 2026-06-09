from app.models.nutrient import Nutrient
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect

from app.db import db
from app.repositories.nutrient_repo import NutrientRepository


class NutrientServiceV0:

    def __init__(self):
        self.repo = NutrientRepository(db)

    def get_all_nutrients(self):
        return self.repo.get_all()

    def get_nutrient_by_id(self, nutrient_id: int):
        return self.repo.get_by_id(nutrient_id)

    def create_nutrient(
        self,
        name: str,
        description: str | None = None,
        image: str | None = None,
        effects: list[HealthEffect] | None = None,
        found_in: list[FoodCategory] | None = None
    ):
        new_id = len(self.repo.get_all()) + 1

        new_nutrient = Nutrient(
            id=new_id,
            name=name,
            description=description,
            image=image,
            effects=effects,
            found_in=found_in
        )

        return self.repo.create(new_nutrient)

    def update_nutrient(
        self,
        nutrient_id: int,
        name: str,
        description: str | None = None,
        image: str | None = None,
        effects: list[HealthEffect] | None = None,
        found_in: list[FoodCategory] | None = None
    ):
        nutrient = self.repo.get_by_id(nutrient_id)

        if not nutrient:
            return None

        nutrient.name = name
        nutrient.description = description
        nutrient.image = image
        nutrient.effects = effects
        nutrient.found_in = found_in

        return nutrient

    def delete_nutrient(self, nutrient_id: int):
        nutrient = self.repo.get_by_id(nutrient_id)

        if not nutrient:
            return None

        self.repo.delete(nutrient_id)

        return {"message": "Nutrient deleted successfully"}
