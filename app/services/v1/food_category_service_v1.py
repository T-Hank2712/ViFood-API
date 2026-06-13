from app.models.food_category import FoodCategory
from app.repositories.food_category_repo import FoodCategoryRepository
from app.helpers.slug import generate_key


class FoodCategoryServiceV1:

    def __init__(self, db):
        self.repo = FoodCategoryRepository(db)
        
    def get_or_create_by_name(self, name: str):
        existing = self.repo._find_by_key(name)

        if existing:
            return existing
        
        key = generate_key(name)

        return self.repo.create(FoodCategory(name=name, key=key))

    def get_all_food_categories(self):
        categories = self.repo.get_all()

        if not categories:
            raise ValueError("Food Category Not Found")

        return categories

    def get_food_category_by_id(self, category_id: str):
        category = self.repo.get_by_id(category_id)

        if not category:
            raise ValueError("Food Category Not Found")

        return category

    def create_food_category(self, name: str):
        existing = self.repo._find_by_key(name)

        if existing:
            raise ValueError("Food Category already exists")

        category = FoodCategory(name=name)
        return self.repo.create(category)

    def update_food_category(self, category_id: str, name: str):
        category = self.repo.get_by_id(category_id)

        if not category:
            raise ValueError("Food Category not found")

        existing = self.repo._find_by_key(name)
        if existing and existing.id != category_id:
            raise ValueError("Food Category already exists")

        return self.repo.update(category_id, name)

    def delete_food_category(self, category_id: str):
        category = self.repo.get_by_id(category_id)

        if not category:
            raise ValueError("Food Category not found")

        success = self.repo.delete(category_id)

        return success
