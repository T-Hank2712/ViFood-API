from datetime import date
import random

from app.schemas.search_schema import SearchNodeResponse
from app.schemas.wiki_node_schema import WikiNodeResponse
from app.services.v1.additive_service_v1 import AdditiveServiceV1
from app.services.v1.ingredient_service_v1 import IngredientServiceV1
from app.services.v1.nutrient_service_v1 import NutrientServiceV1


class SearchServiceV1:
    def __init__(self, db):
        self.nutrient_service = NutrientServiceV1(db)
        self.ingredient_service = IngredientServiceV1(db)
        self.additive_service = AdditiveServiceV1(db)

    def _map_node(self, node: WikiNodeResponse, node_type: str) -> SearchNodeResponse:
        return SearchNodeResponse(
            id=node.id,
            name=node.name,
            type=node_type,
            sections=node.sections,
        )

    def get_all(self) -> list[SearchNodeResponse]:
        results: list[SearchNodeResponse] = []

        results.extend([
            self._map_node(nutrient, "nutrient")
            for nutrient in self.nutrient_service.get_all_nutrients()
        ])
        results.extend([
            self._map_node(ingredient, "ingredient")
            for ingredient in self.ingredient_service.get_all_ingredients()
        ])
        results.extend([
            self._map_node(additive, "additive")
            for additive in self.additive_service.get_all_additives()
        ])

        random.shuffle(results)

        return results

    def get_by_id(self, id: str) -> SearchNodeResponse | None:
        node_type = self._get_node_type(id)

        try:
            if node_type == "nutrient":
                nutrient = self.nutrient_service.get_nutrient_by_id(id)
                return self._map_node(nutrient, node_type)

            if node_type == "ingredient":
                ingredient = self.ingredient_service.get_ingredient_by_id(id)
                return self._map_node(ingredient, node_type)

            if node_type == "additive":
                additive = self.additive_service.get_additive_by_id(id)
                return self._map_node(additive, node_type)
        except ValueError:
            return None

        return None

    def _get_node_type(self, id: str) -> str | None:
        if id.startswith("NUTRIENT:"):
            return "nutrient"

        if id.startswith("INGREDIENT:"):
            return "ingredient"

        if id.startswith("ADDITIVE:"):
            return "additive"

        return None

    def get_daily_feature(self) -> SearchNodeResponse | None:
        items = self.get_all()

        if not items:
            return None

        rng = random.Random(2025)
        rng.shuffle(items)

        index = date.today().toordinal() % len(items)
        return items[index]
