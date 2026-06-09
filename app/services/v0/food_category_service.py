from app.models.food_category import FoodCategory
from app.repositories.food_category_repo import FoodCategoryRepository
from app.db import db


class FoodCategoryServiceV0:
    
    def __init__(self):
        self.repo = FoodCategoryRepository(db)

    def get_all_food_categories(self):
        return self.repo.get_all()

    def get_food_category_by_id(self, food_category_id: int):
        return self.repo.get_by_id(food_category_id)

    def create_food_category(self, name: str):
        new_id = len(self.repo.get_all()) + 1

        new_food_category = FoodCategory(
            id=new_id,
            name=name
        )

        return self.repo.add(new_food_category)

    def update_food_category(self, food_category_id: int, name: str):
        food_category = self.repo.get_by_id(food_category_id)

        if not food_category:
            return None

        # update field (fake DB nên mutate trực tiếp OK)
        food_category.name = name
        return food_category

    def delete_food_category(self, food_category_id: int):
        food_category = self.repo.get_by_id(food_category_id)

        if not food_category:
            return None

        self.repo.delete(food_category_id)
        return {"message": "Food category deleted successfully"}
