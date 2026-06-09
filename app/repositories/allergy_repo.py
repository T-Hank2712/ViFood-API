from app.models.allergy import Allergy


class AllergyRepository:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.allergies

    def get_by_id(self, additive_id: int):
        return next((a for a in self.db.allergies if a.id == additive_id), None)

    def create(self, allergy: Allergy):
        self.db.allergies.append(allergy)
        return allergy

    def delete(self, allergy_id: int):
        self.db.allergies = [
            a for a in self.db.allergies if a.id != allergy_id
        ]
        return True
