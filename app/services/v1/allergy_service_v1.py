from app.models.allergy import Allergy
from app.repositories.allergy_repo import AllergyRepository


class AllergyServiceV1:

    def __init__(self, db):
        self.repo = AllergyRepository(db)

    def get_all_allergies(self):
        allergies = self.repo.get_all()

        if not allergies:
            raise ValueError("Allergy Not Found")

        return allergies

    def get_allergy_by_id(self, allergy_id: str):
        allergy = self.repo.get_by_id(allergy_id)

        if not allergy:
            raise ValueError("Allergy Not Found")

        return allergy

    def create_allergy(self, name: str):
        existing = self.repo._find_by_key(name)

        if existing:
            raise ValueError("Allergy already exists")

        allergy = Allergy(name=name)
        return self.repo.create(allergy)

    def update_allergy(self, allergy_id: str, name: str):
        allergy = self.repo.get_by_id(allergy_id)

        if not allergy:
            raise ValueError("Allergy not found")

        existing = self.repo._find_by_key(name)

        if existing and existing.id != allergy_id:
            raise ValueError("Allergy already exists")

        return self.repo.update(allergy_id, name)

    def delete_allergy(self, allergy_id: str):
        allergy = self.repo.get_by_id(allergy_id)

        if not allergy:
            raise ValueError("Allergy not found")

        self.repo.delete(allergy_id)

        return {
            "message": "Allergy deleted successfully"
        }
