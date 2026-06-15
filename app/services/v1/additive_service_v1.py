from app.models.additive import Additive
from app.repositories.additive_repo import AdditiveRepository
from app.schemas.additive_schema import CreateAdditiveRequest, UpdateAdditiveRequest
from app.services.v1.health_effect_service_v1 import HealthEffectServiceV1
from app.services.v1.food_category_service_v1 import FoodCategoryServiceV1
from app.schemas.effect_schema import HealthEffectRequest
from app.schemas.profile_schema import HealthProfileRequest


class AdditiveServiceV1:

    def __init__(self, db):
        self.repo = AdditiveRepository(db)
        self.effect_service = HealthEffectServiceV1(db)
        self.food_category_service = FoodCategoryServiceV1(db)

    def get_all_additives(self):
        additives = self.repo.get_all()

        if not additives:
            raise ValueError("Additive Not Found")

        return additives

    def get_additive_by_id(self, additive_id: str):
        additive = self.repo.get_by_id(additive_id)

        if not additive:
            raise ValueError("Additive Not Found")

        return additive

    def create_additive(self, payload: CreateAdditiveRequest):
        existing = self.repo._find_by_key(payload.name)

        if existing:
            raise ValueError("Additive already exist")

        additive = Additive(
            name=payload.name,
            code=payload.code,
            description=payload.description
        )

        return self.repo.create(additive)

    def update_additive(self, additive_id: str, payload: UpdateAdditiveRequest):
        additive = self.repo.get_by_id(additive_id)

        if not additive:
            raise ValueError("Additive not found")

        existing = self.repo._find_by_key(payload.name)

        if existing and existing.id != additive_id:
            raise ValueError("Additive already exists")

        updated_additive = Additive(
            name=payload.name,
            code=payload.code,
            description=payload.description
        )

        return self.repo.update(additive_id, updated_additive)

    def delete_additive(self, additive_id: str):
        additive = self.repo.get_by_id(additive_id)

        if not additive:
            raise ValueError("Additive not found")

        success = self.repo.delete(additive_id)

        return success

    def attach_effect_to_additive(
        self,
        additive_id: str,
        effect: HealthEffectRequest
    ):

        additive = self.repo.get_by_id(additive_id)

        if not additive:
            raise ValueError("Additive not found")

        health_effect = self.effect_service.get_or_create_by_title(
            effect.title
        )

        self.repo.attach_effect(additive_id, health_effect.id)

        return True

    def attach_category_to_additive(
        self,
        additive_id: str,
        category: HealthProfileRequest
    ):

        additive = self.repo.get_by_id(additive_id)

        if not additive:
            raise ValueError("Additive not found")

        category_node = self.food_category_service.get_or_create_by_name(
            category.name
        )

        self.repo.attach_category(additive_id, category_node.id)

        return True
