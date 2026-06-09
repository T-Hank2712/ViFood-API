from app.models.disease import Disease


class DiseaseRepository:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.diseases

    def get_by_id(self, disease_id: int):
        return next((d for d in self.db.diseases if d.id == disease_id), None)
    
    def create(self, disease: Disease):
        self.db.diseases.append(disease)
        return disease

    def delete(self, disease_id: int):
        self.db.diseases = [
            d for d in self.db.diseases if d.id != disease_id
        ]
        return True
