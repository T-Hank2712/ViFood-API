from app.models.disease import Disease
from app.repositories.disease_repo import DiseaseRepository


class DiseaseServiceV1:

    def __init__(self, db):
        self.repo = DiseaseRepository(db)

    def get_all_diseases(self):
        diseases = self.repo.get_all()

        if not diseases:
            raise ValueError("Disease Not Found")

        return diseases

    def get_disease_by_id(self, disease_id: str):
        disease = self.repo.get_by_id(disease_id)

        if not disease:
            raise ValueError("Disease Not Found")

        return disease

    def create_disease(self, name: str):
        existing = self.repo._find_by_key(name)

        if existing:
            raise ValueError("Disease already exists")

        disease = Disease(name=name)
        return self.repo.create(disease)

    def update_disease(self, disease_id: str, name: str):
        disease = self.repo.get_by_id(disease_id)

        if not disease:
            raise ValueError("Disease not found")

        existing = self.repo._find_by_key(name)
        if existing and existing.id != disease_id:
            raise ValueError("Disease already exists")

        return self.repo.update(disease_id, name)

    def delete_disease(self, disease_id: str):
        disease = self.repo.get_by_id(disease_id)

        if not disease:
            raise ValueError("Disease not found")

        self.repo.delete(disease_id)

        return {
            "message": "Disease deleted successfully"
        }
