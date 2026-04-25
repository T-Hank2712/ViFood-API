from app.models.allergy import Allergy

allergies = [
    Allergy(id=1, name="Sữa"),
    Allergy(id=2, name="Gluten"),
    Allergy(id=3, name="Đậu phộng")]


class AllergyServiceV0:

    @staticmethod
    def get_all_allergies(): return allergies

    @staticmethod
    def get_allergy_by_id(allergy_id: int):
        return next((a for a in allergies if a.id == allergy_id), None)
    
    @staticmethod
    def create_allergy(name: str):
        new_id = max(a.id for a in allergies) + 1 if allergies else 1
        new_allergy = Allergy(id=new_id, name=name)
        allergies.append(new_allergy)
        return new_allergy
    
    @staticmethod
    def update_allergy(allergy_id: int, name: str):
        allergy = AllergyServiceV0.get_allergy_by_id(allergy_id)
        if allergy:
            allergy.name = name
            return allergy
        return None
    
    @staticmethod
    def delete_allergy(allergy_id: int):
        global allergies
        allergies = [a for a in allergies if a.id != allergy_id]
        return {"message": "Allergy deleted successfully"}
