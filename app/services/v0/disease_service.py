# from app.models.disease import Disease
# from app.repositories.disease_repo import DiseaseRepository
# from app.db import db


# class DiseaseServiceV0:

#     def __init__(self):
#         self.repo = DiseaseRepository(db)

#     def get_all_diseases(self):
#         return self.repo.get_all()

#     def get_disease_by_id(self, disease_id: int):
#         return self.repo.get_by_id(disease_id)

#     def create_disease(
#         self,
#         name: str
#     ):
#         new_id = len(self.repo.get_all()) + 1

#         new_disease = Disease(
#             id=new_id,
#             name=name,
#         )

#         return self.repo.create(new_disease)

#     def update_disease(
#         self,
#         disease_id: int,
#         name: str,
#     ):
#         disease = self.repo.get_by_id(disease_id)

#         if not disease:
#             return None

#         disease.name = name

#         return disease

#     def delete_disease(self, disease_id: int):
#         return self.repo.delete(disease_id)
