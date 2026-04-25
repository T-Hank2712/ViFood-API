from app.models.additive import Additive

additives = [
    Additive(id=1, name="E100", description="Curcumin - chất tạo màu vàng tự nhiên"),
    Additive(id=2, name="E200", description="Sorbic Acid - chất bảo quản chống nấm mốc"),
    Additive(id=3, name="E300", description="Ascorbic Acid - chất chống oxy hóa")]


class AdditiveServiceV0:
    
    @staticmethod
    def get_all_additives(): return additives

    @staticmethod
    def get_additive_by_id(additive_id: int):
        return next((a for a in additives if a.id == additive_id), None)
    
    @staticmethod
    def create_additive(name: str, description: str | None = None):
        new_id = max(a.id for a in additives) + 1 if additives else 1
        new_additive = Additive(id=new_id, name=name, description=description)
        additives.append(new_additive)
        return new_additive
    
    @staticmethod
    def update_additive(additive_id: int, name: str, description: str | None = None):
        additive = AdditiveServiceV0.get_additive_by_id(additive_id)
        if additive:
            additive.name = name
            additive.description = description
            return additive
        return None
    
    @staticmethod
    def delete_additive(additive_id: int):
        global additives
        additives = [a for a in additives if a.id != additive_id]
        return {"message": "Additive deleted successfully"}
