from app.models.ingredient import Ingredient
from app.repositories.ingredient_repo import IngredientRepository
from app.schemas.ingredient_schema import CreateIngredientRequest, UpdateIngredientRequest
from app.services.v1.health_effect_service_v1 import HealthEffectServiceV1
from app.services.v1.food_category_service_v1 import FoodCategoryServiceV1
from app.schemas.effect_schema import HealthEffectRequest
from app.schemas.profile_schema import HealthProfileRequest


class IngredientServiceV1:

    def __init__(self, db):
        self.repo = IngredientRepository(db)
        self.effect_service = HealthEffectServiceV1(db)
        self.food_category_service = FoodCategoryServiceV1(db)

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
    
    def get_ingredient_detail(self, ingredient_id: str):
        ingredient = self.repo.get_ingredient_detail(ingredient_id)

        if not ingredient:
            raise ValueError("Ingredient Not Found")

        return ingredient

    def create_ingredient(self, payload: CreateIngredientRequest):
        existing = self.repo._find_by_key(payload.name)
        
        print("existing =", existing)

        if existing:
            raise ValueError("Ingredient already exists")

        ingredient = Ingredient(
            name=payload.name,
            description=payload.description
        )

        return self.repo.create(ingredient)

    def update_ingredient(
        self,
        ingredient_id: str,
        payload: UpdateIngredientRequest
    ):
        ingredient = self.repo.get_by_id(ingredient_id)

        if not ingredient:
            raise ValueError("Ingredient not found")

        existing = self.repo._find_by_key(payload.name)

        if existing and existing.id != ingredient_id:
            raise ValueError("Ingredient already exists")

        updated_ingredient = Ingredient(
            name=payload.name,
            description=payload.description
        )

        return self.repo.update(
            ingredient_id,
            updated_ingredient
        )

    def delete_ingredient(self, ingredient_id: str):
        ingredient = self.repo.get_by_id(ingredient_id)

        if not ingredient:
            raise ValueError("Ingredient not found")

        return self.repo.delete(ingredient_id)

    def attach_effect_to_ingredient(
        self,
        ingredient_id: str,
        effect: HealthEffectRequest
    ):
        ingredient = self.repo.get_by_id(ingredient_id)

        if not ingredient:
            raise ValueError("Ingredient not found")

        health_effect = self.effect_service.get_or_create_by_name(
            effect.name
        )

        self.repo.attach_effect(
            ingredient_id,
            health_effect.id
        )

        return True

    def attach_category_to_ingredient(
        self,
        ingredient_id: str,
        category: HealthProfileRequest
    ):
        ingredient = self.repo.get_by_id(ingredient_id)

        if not ingredient:
            raise ValueError("Ingredient not found")

        category_node = (
            self.food_category_service.get_or_create_by_name(
                category.name
            )
        )

        self.repo.attach_category(
            ingredient_id,
            category_node.id
        )

        return True
