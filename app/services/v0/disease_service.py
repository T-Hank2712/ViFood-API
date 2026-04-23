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