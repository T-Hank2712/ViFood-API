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
            name=getattr(node, "name_vi", None) or node.name,
            type=node_type,
            sections=getattr(node, "sections", []),
        )

    def _get_nodes_by_type(self, getter, node_type: str) -> list[SearchNodeResponse]:
        try:
            return [
                self._map_node(node, node_type)
                for node in getter()
            ]
        except ValueError:
            return []

    def _get_all_nodes(self) -> list[SearchNodeResponse]:
        results: list[SearchNodeResponse] = []

        results.extend(self._get_nodes_by_type(
            self.nutrient_service.get_all_nutrients,
            "nutrient",
        ))
        results.extend(self._get_nodes_by_type(
            self.ingredient_service.get_all_ingredients,
            "ingredient",
        ))
        results.extend(self._get_nodes_by_type(
            self.additive_service.get_all_additives,
            "additive",
        ))

        return results

    def get_all(self) -> list[SearchNodeResponse]:
        results = self._get_all_nodes()
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
        items = sorted(self._get_all_nodes(), key=lambda item: item.id)

        if not items:
            return None

        rng = random.Random(2025)
        rng.shuffle(items)

        index = date.today().toordinal() % len(items)
        return items[index]
