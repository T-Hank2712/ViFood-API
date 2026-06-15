from app.models.DTOs.searchDTO import searchDTO
from app.models.additive import Additive
from app.models.ingredient import Ingredient
from app.models.nutrient import Nutrient

from app.services.v1.additive_service_v1 import AdditiveServiceV1
from app.services.v1.ingredient_service_v1 import IngredientServiceV1
from app.services.v1.nutrient_service_v1 import NutrientServiceV1
import random


class SearchServiceV1:
    def __init__(self, db):
        self.nutrient_service = NutrientServiceV1(db)
        self.ingredient_service = IngredientServiceV1(db)
        self.additive_service = AdditiveServiceV1(db)
        
    def map_nutrient(self, n: Nutrient) -> searchDTO:
        return searchDTO(
            id=f"nutrient-{n.id}",
            name=n.name,
            key=n.key,
            description=n.description,
            type="nutrient"
        )
        
    def map_ingredient(self, i: Ingredient) -> searchDTO:
        return searchDTO(
            id=f"ingredient-{i.id}",
            name=i.name,
            key=i.key,
            description=i.description,
            type="ingredient"
        )

    def map_additive(self, a: Additive) -> searchDTO:
        return searchDTO(
            id=f"additive-{a.id}",
            name=a.name,
            key=a.key,
            code=a.code,
            description=a.description,
            type="additive"
        )
        
    def get_all(self) -> list[searchDTO]:
        results: list[searchDTO] = []

        # Nutrients
        nutrients = self.nutrient_service.get_all_nutrients()
        results.extend([self.map_nutrient(n) for n in nutrients])

        # Ingredients
        ingredients = self.ingredient_service.get_all_ingredients()
        results.extend([self.map_ingredient(i) for i in ingredients])

        # Additives
        additives = self.additive_service.get_all_additives()
        results.extend([self.map_additive(a) for a in additives])

        random.shuffle(results)

        return results
    
    def get_by_id(self, id: str) -> searchDTO | None:
        try:
            prefix, id_str = id.split("-", 1)
        except ValueError:
            return None

        if prefix == "nutrient":
            n = self.nutrient_service.get_nutrient_by_id(id_str)
            return self.map_nutrient(n) if n else None

        elif prefix == "ingredient":
            i = self.ingredient_service.get_ingredient_by_id(id_str)
            return self.map_ingredient(i) if i else None

        elif prefix == "additive":
            a = self.additive_service.get_additive_by_id(id_str)
            return self.map_additive(a) if a else None

        return None
