from app.repositories.nutrient_repo import NutrientRepository


class NutrientServiceV1:

    def __init__(self, db):
        self.repo = NutrientRepository(db)

    def get_all_nutrients(self):
        nutrients = self.repo.get_all()

        if not nutrients:
            raise ValueError("Nutrient Not Found")

        return nutrients

    def get_nutrient_by_id(self, nutrient_id: str):
        nutrient = self.repo.get_by_id(nutrient_id)

        if not nutrient:
            raise ValueError("Nutrient Not Found")

        return nutrient
