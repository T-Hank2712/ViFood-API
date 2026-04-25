from app.models.nutrient import Nutrient

nutrients = [
    Nutrient(id=1, name="Protein", description="Chất đạm giúp xây dựng cơ bắp"),
    Nutrient(id=2, name="Carbohydrate", description="Tinh bột cung cấp năng lượng"),
    Nutrient(id=3, name="Fat", description="Chất béo hỗ trợ hấp thụ vitamin")]


class NutrientServiceV0:

    @staticmethod
    def get_all_nutrients(): return nutrients

    @staticmethod
    def get_nutrient_by_id(nutrient_id: int):
        return next((n for n in nutrients if n.id == nutrient_id), None)
    
    @staticmethod
    def create_nutrient(name: str, description: str | None = None):
        new_id = max(n.id for n in nutrients) + 1 if nutrients else 1
        new_nutrient = Nutrient(id=new_id, name=name, description=description)
        nutrients.append(new_nutrient)
        return new_nutrient
    
    @staticmethod
    def update_nutrient(nutrient_id: int, name: str, description: str | None = None):
        nutrient = NutrientServiceV0.get_nutrient_by_id(nutrient_id)
        if nutrient:
            nutrient.name = name
            nutrient.description = description
            return nutrient
        return None
    
    @staticmethod
    def delete_nutrient(nutrient_id: int):
        global nutrients
        nutrients = [n for n in nutrients if n.id != nutrient_id]
        return {"message": "Nutrient deleted successfully"}
