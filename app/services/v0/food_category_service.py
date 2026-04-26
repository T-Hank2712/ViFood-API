from app.models.food_category import FoodCategory

foodCategories = [
    FoodCategory(id=1, name="Trái cây"),
    FoodCategory(id=2, name="Rau củ"),
    FoodCategory(id=3, name="Ngũ cốc")]


class FoodCategoryServiceV0:
    @staticmethod
    def get_all_food_categories():
        return foodCategories
    
    @staticmethod
    def get_food_category_by_id(food_category_id: int):
        return next((n for n in foodCategories if n.id == food_category_id), None)

    @staticmethod
    def create_food_category(name: str):
        new_id = max(n.id for n in foodCategories) + 1 if foodCategories else 1
        new_food_category = FoodCategory(id=new_id, name=name)
        foodCategories.append(new_food_category)
        return new_food_category
    
    @staticmethod
    def update_food_category(food_category_id: int, name: str):
        food_category = FoodCategoryServiceV0.get_food_category_by_id(food_category_id)
        if food_category:
            food_category.name = name
            return food_category
        return None
    
    @staticmethod
    def delete_food_category(food_category_id: int):
        global foodCategories
        foodCategories = [n for n in foodCategories if n.id != food_category_id]
        return {"message": "Food category deleted successfully"}
