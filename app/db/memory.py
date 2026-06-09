from typing import List
from app.models.allergy import Allergy
from app.models.disease import Disease
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect
from app.models.health_goal import HealthGoal
from app.models.product import Product
from app.models.ingredient import Ingredient
from app.models.additive import Additive
from app.models.nutrient import Nutrient
from app.models.user import User
from app.models.user_profile import UserProfile


class FakeDB:
    def __init__(self):
        # =====================
        # STORAGE TABLES
        # =====================
        self.products: List[Product] = []
        self.ingredients: List[Ingredient] = []
        self.additives: List[Additive] = []
        self.nutrients: List[Nutrient] = []
        self.users: List[User] = []
        self.user_profiles: List[UserProfile] = []
        self.allergies: List[Allergy] = []
        self.diseases: List[Disease] = []
        self.health_goals: List[HealthGoal] = []
        self.food_categories: List[FoodCategory] = []
        self.health_effects: List[HealthEffect] = []

        # =====================
        # OPTIONAL INDEX (tăng tốc lookup)
        # =====================
        self.ingredient_index = {}
        self.additive_index = {}
        self.nutrient_index = {}
        self.product_index = {}

    # =====================
    # NORMALIZE KEY
    # =====================
    def _key(self, value: str) -> str:
        return value.strip().lower()

    # =====================
    # INGREDIENT
    # =====================
    def find_ingredient(self, name: str):
        return self.ingredient_index.get(self._key(name))

    def save_ingredient(self, ingredient: Ingredient):
        key = self._key(ingredient.name)
        self.ingredient_index[key] = ingredient
        self.ingredients.append(ingredient)
        return ingredient

    # =====================
    # ADDITIVE
    # =====================
    def find_additive(self, name: str):
        return self.additive_index.get(self._key(name))

    def save_additive(self, additive: Additive):
        key = self._key(additive.name)
        self.additive_index[key] = additive
        self.additives.append(additive)
        return additive

    # =====================
    # NUTRIENT
    # =====================
    def find_nutrient(self, name: str):
        return self.nutrient_index.get(self._key(name))

    def save_nutrient(self, nutrient: Nutrient):
        key = self._key(nutrient.name)
        self.nutrient_index[key] = nutrient
        self.nutrients.append(nutrient)
        return nutrient

    # =====================
    # PRODUCT
    # =====================
    def save_product(self, product: Product):
        self.product_index[product._id] = product
        self.products.append(product)
        return product

    def find_product_by_id(self, product_id: int):
        return self.product_index.get(product_id)
