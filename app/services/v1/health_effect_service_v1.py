from app.models.health_effect import HealthEffect
from app.repositories.health_effect_repo import HealthEffectRepository
from app.schemas.effect_schema import HealthEffectRequest
from app.helpers.slug import generate_key


class HealthEffectServiceV1:

    def __init__(self, db):
        self.repo = HealthEffectRepository(db)
        
    def get_or_create_by_title(self, title: str):
        existing = self.repo._find_by_key(title)

        if existing:
            return existing
        
        key = generate_key(title)

        effect = HealthEffect(
            title=title,
            key=key
        )

        return self.repo.create(effect)

    def get_all_health_effects(self):
        effects = self.repo.get_all()

        if not effects:
            raise ValueError("Health Effect Not Found")

        return effects

    def get_health_effect_by_id(self, effect_id: str):
        effect = self.repo.get_by_id(effect_id)

        if not effect:
            raise ValueError("Health Effect Not Found")

        return effect

    def create_health_effect(
        self,
        title: str,
        description: str
    ):
        existing = self.repo._find_by_key(title)

        if existing:
            raise ValueError("Health Effect already exists")

        effect = HealthEffect(
            title=title,
            description=description
        )

        return self.repo.create(effect)

    def update_health_effect(
        self,
        effect_id: str,
        payload: HealthEffectRequest
    ):
        effect = self.repo.get_by_id(effect_id)

        if not effect:
            raise ValueError("Health Effect not found")

        new_title = (
            payload.title
            if payload.title is not None
            else effect.title
        )

        new_description = (
            payload.description
            if payload.description is not None
            else effect.description
        )

        existing = self.repo._find_by_key(new_title)

        if existing and existing.id != effect_id:
            raise ValueError("Health Effect already exists")

        return self.repo.update(
            effect_id=effect_id,
            title=new_title,
            description=new_description
        )

    def delete_health_effect(self, effect_id: str):
        effect = self.repo.get_by_id(effect_id)

        if not effect:
            raise ValueError("Health Effect not found")

        return self.repo.delete(effect_id)
