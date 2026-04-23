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