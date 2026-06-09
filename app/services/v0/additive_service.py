from app.models.additive import Additive
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect
from app.repositories.additive_repo import AdditiveRepository
from app.db import db


class AdditiveServiceV0:

    def __init__(self):
        self.repo = AdditiveRepository(db)

    def get_all_additives(self):
        return self.repo.get_all()

    def get_additive_by_id(self, additive_id: int):
        return self.repo.get_by_id(additive_id)

    def create_additive(
        self,
        name: str,
        description: str | None = None,
        code: str | None = None,
        image: str | None = None,
        effects: list[HealthEffect] | None = None,
        found_in: list[FoodCategory] | None = None
    ):
        new_id = len(self.repo.get_all()) + 1

        new_additive = Additive(
            id=new_id,
            name=name,
            code=code,
            description=description,
            image=image,
            effects=effects or [],
            found_in=found_in or []
        )

        return self.repo.create(new_additive)

    def update_additive(
        self,
        additive_id: int,
        name: str,
        description: str | None = None,
        code: str | None = None,
        image: str | None = None,
        effects: list[HealthEffect] | None = None,
        found_in: list[FoodCategory] | None = None
    ):
        additive = self.repo.get_by_id(additive_id)

        if not additive:
            return None

        additive.name = name
        additive.description = description
        additive.code = code
        additive.image = image
        additive.effects = effects or []
        additive.found_in = found_in or []

        return additive

    def delete_additive(self, additive_id: int):
        return self.repo.delete(additive_id)
