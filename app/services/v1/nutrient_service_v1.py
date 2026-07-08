from app.repositories.nutrient_repo import NutrientRepository
from app.templates.nutrient_section_template import build_nutrient_sections


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

        nutrient.sections = build_nutrient_sections(nutrient)
        return nutrient
