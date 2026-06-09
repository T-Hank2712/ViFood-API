from app.models.food_category import FoodCategory


class FoodCategoryRepository:
    
    def __init__(self, db):
        self.db = db
    
    def get_all(self):
        return self.db.food_categories

    def get_by_id(self, food_category_id: int):
        return next(
            (n for n in self.db.food_categories if n.id == food_category_id),
            None
        )

    def add(self, food_category: FoodCategory):
        self.db.food_categories.append(food_category)
        return food_category

    def delete(self, food_category_id: int):
        self.db.food_categories = [
            n for n in self.db.food_categories if n.id != food_category_id
        ]
