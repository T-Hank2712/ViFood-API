from app.models.disease import Disease

diseases = [
    Disease(id=1, name="Bệnh tiểu đường"),
    Disease(id=2, name="Bệnh tim mạch"),
    Disease(id=3, name="Bệnh béo phì"),
]


class DiseaseServiceV0:

    @staticmethod
    def get_all():
        return diseases

    @staticmethod
    def get_by_id(disease_id: int):
        return next((d for d in diseases if d.id == disease_id), None)
    
    @staticmethod
    def create_disease(name: str):
        new_id = max(d.id for d in diseases) + 1 if diseases else 1
        new_disease = Disease(id=new_id, name=name)
        diseases.append(new_disease)
        return new_disease
    
    @staticmethod
    def update_disease(disease_id: int, name: str):
        disease = next((d for d in diseases if d.id == disease_id), None)
        if disease:
            disease.name = name
            return disease
        return None
    
    @staticmethod
    def delete_disease(disease_id: int):
        global diseases
        diseases = [d for d in diseases if d.id != disease_id]
        return {"message": "Disease deleted successfully"}
