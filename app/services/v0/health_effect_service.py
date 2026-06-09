from app.models.health_effect import HealthEffect
from app.repositories.health_effect_repo import HealthEffectRepository
from app.db import db


class HealthEffectServiceV0:

    def __init__(self):
        self.repo = HealthEffectRepository(db)

    def get_all_health_effects(self):
        return self.repo.get_all()

    def get_health_effect_by_id(self, health_effect_id: int):
        return self.repo.get_by_id(health_effect_id)

    def create_health_effect(self, title: str):
        new_id = len(self.repo.get_all()) + 1

        new_health_effect = HealthEffect(
            id=new_id,
            title=title
        )

        return self.repo.create(new_health_effect)

    def update_health_effect(self, health_effect_id: int, title: str):
        health_effect = self.repo.get_by_id(health_effect_id)

        if not health_effect:
            return None

        health_effect.title = title
        return health_effect

    def delete_health_effect(self, health_effect_id: int):
        health_effect = self.repo.get_by_id(health_effect_id)

        if not health_effect:
            return None

        self.repo.delete(health_effect_id)

        return {"message": "Health effect deleted successfully"}
