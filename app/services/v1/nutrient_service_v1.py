from app.models.nutrient import Nutrient
from app.repositories.nutrient_repo import NutrientRepository
from app.schemas.nutrient_schema import CreateNutrientRequest, UpdateNutrientRequest
from app.services.v1.health_effect_service_v1 import HealthEffectServiceV1
from app.services.v1.food_category_service_v1 import FoodCategoryServiceV1
from app.schemas.effect_schema import HealthEffectRequest
from app.schemas.profile_schema import HealthProfileRequest


class NutrientServiceV1:

    def __init__(self, db):
        self.repo = NutrientRepository(db)
        self.effect_service = HealthEffectServiceV1(db)
        self.food_category_service = FoodCategoryServiceV1(db)

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
    
    def get_nutrient_detail(self, nutrient_id: str):
        nutrient = self.repo.get_nutrient_detail(nutrient_id)

        if not nutrient:
            raise ValueError("Nutrient Not Found")

        return nutrient

    def create_nutrient(self, payload: CreateNutrientRequest):
        existing = self.repo._find_by_key(payload.name)

        if existing:
            raise ValueError("Nutrient already exist")

        nutrient = Nutrient(name=payload.name, description=payload.description)
        return self.repo.create(nutrient)
    
    def update_nutrient(self, nutrient_id: str, payload: UpdateNutrientRequest):
        nutrient = self.repo.get_by_id(nutrient_id)

        if not nutrient:
            raise ValueError("Nutrient not found")

        existing = self.repo._find_by_key(payload.name)
        if existing and existing.id != nutrient_id:
            raise ValueError("Nutrient already exists")

        updated_nutrient = Nutrient(
            name=payload.name,
            description=payload.description
        )

        return self.repo.update(nutrient_id, updated_nutrient)

    def delete_nutrient(self, nutrient_id: str):
        nutrient = self.repo.get_by_id(nutrient_id)

        if not nutrient:
            raise ValueError("Nutrient not found")

        success = self.repo.delete(nutrient_id)

        return success
    
    def attach_effect_to_nutrient(self, nutrient_id: str, effect: HealthEffectRequest):
        
        nutrient = self.repo.get_by_id(nutrient_id)

        if not nutrient:
            raise ValueError("Nutrient not found")
        
        health_effect = self.effect_service.get_or_create_by_name(effect.name)
        
        self.repo.attach_effect(nutrient_id, health_effect.id)
        
        return True
    
    def attach_category_to_nutrient(self, nutrient_id: str, category: HealthProfileRequest):
    
        nutrient = self.repo.get_by_id(nutrient_id)

        if not nutrient:
            raise ValueError("Nutrient not found")
        
        category_node = self.food_category_service.get_or_create_by_name(category.name)
        
        self.repo.attach_category(nutrient_id, category_node.id)
        
        return True
