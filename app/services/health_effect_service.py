from app.models.health_effect import HealthEffect

healthEffects = [
    HealthEffect(id=1, title="Tăng cường hệ miễn dịch"),
    HealthEffect(id=2, title="Hỗ trợ tiêu hóa"),
    HealthEffect(id=3, title="Giảm nguy cơ mắc bệnh tim mạch")]


class HealthEffectServiceV0:
    @staticmethod
    def get_all_health_effects():
        return healthEffects
    
    @staticmethod
    def get_health_effect_by_id(health_effect_id: int):
        return next((n for n in healthEffects if n.id == health_effect_id), None)

    @staticmethod
    def create_health_effect(title: str):
        new_id = max(n.id for n in healthEffects) + 1 if healthEffects else 1
        new_health_effect = HealthEffect(id=new_id, title=title)
        healthEffects.append(new_health_effect)
        return new_health_effect
    
    @staticmethod
    def update_health_effect(health_effect_id: int, title: str):
        health_effect = HealthEffectServiceV0.get_health_effect_by_id(health_effect_id)
        if health_effect:
            health_effect.title = title
            return health_effect
        return None
    
    @staticmethod
    def delete_health_effect(health_effect_id: int):
        global healthEffects
        healthEffects = [n for n in healthEffects if n.id != health_effect_id]
        return {"message": "Health effect deleted successfully"}
