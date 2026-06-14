# from app.models.ingredient import Ingredient
# from app.models.food_category import FoodCategory
# from app.models.health_effect import HealthEffect

# from app.db import db
# from app.repositories.ingredient_repo import IngredientRepository


# class IngredientServiceV0:

#     def __init__(self):
#         self.repo = IngredientRepository(db)

#     def get_all_ingredients(self):
#         return self.repo.get_all()

#     def get_ingredient_by_id(self, ingredient_id: int):
#         return self.repo.get_by_id(ingredient_id)

#     def create_ingredient(
#         self,
#         name: str,
#         description: str | None = None,
#         image: str | None = None,
#         effects: list[HealthEffect] | None = None,
#         found_in: list[FoodCategory] | None = None
#     ):
#         new_id = len(self.repo.get_all()) + 1

#         new_ingredient = Ingredient(
#             id=new_id,
#             name=name,
#             description=description,
#             image=image,
#             effects=effects,
#             found_in=found_in
#         )

#         return self.repo.create(new_ingredient)

#     def update_ingredient(
#         self,
#         ingredient_id: int,
#         name: str,
#         description: str | None = None,
#         image: str | None = None,
#         effects: list[HealthEffect] | None = None,
#         found_in: list[FoodCategory] | None = None
#     ):
#         ingredient = self.repo.get_by_id(ingredient_id)

#         if not ingredient:
#             return None

#         ingredient.name = name
#         ingredient.description = description
#         ingredient.image = image
#         ingredient.effects = effects
#         ingredient.found_in = found_in

#         return ingredient

#     def delete_ingredient(self, ingredient_id: int):
#         return self.repo.delete(ingredient_id)
