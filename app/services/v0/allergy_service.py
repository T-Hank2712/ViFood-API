# from app.models.allergy import Allergy
# from app.repositories.allergy_repo import AllergyRepository
# from app.db import db


# class AllergyServiceV0:

#     def __init__(self):
#         self.repo = AllergyRepository(db)

#     def get_all_allergies(self):
#         return self.repo.get_all()

#     def get_allergy_by_id(self, allergy_id: int):
#         return self.repo.get_by_id(allergy_id)
    
#     def create_allergy(
#         self,
#         name: str
#     ):
#         new_id = len(self.repo.get_all()) + 1

#         new_allergy = Allergy(
#             id=new_id,
#             name=name
#         )

#         return self.repo.create(new_allergy)

#     def update_allergy(
#         self,
#         allergy_id: int,
#         name: str
#     ):
#         allergy = self.repo.get_by_id(allergy_id)

#         if not allergy:
#             return None

#         allergy.name = name

#         return allergy

#     def delete_allergy(self, allergy_id: int):
#         return self.repo.delete(allergy_id)
