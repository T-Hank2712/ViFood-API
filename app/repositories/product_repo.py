from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.models.product import Product

utc_now = datetime.now(timezone.utc)


class ProductRepository:
    
    def __init__(self, db):
        self.db = db

    def get_all(self, user_id: int) -> list[Product]:
        return [
            product
            for product in self.db.products
            if product.user_id == user_id
        ]

    def get_by_id(self, product_id: int, user_id: int) -> Product | None:
        for product in self.db.products:
            if product.id == product_id and product.user_id == user_id:
                return product
        return None

    def count(self, user_id: int) -> int:
        return len([
            product
            for product in self.db.products
            if product.user_id == user_id
        ])

    def count_by_date(self, user_id: int, day: int, month: int, year: int) -> int:
        return len([
            product
            for product in self.db.products
            if product.user_id == user_id
            and product.createdAtLocal.day == day
            and product.createdAtLocal.month == month
            and product.createdAtLocal.year == year
        ])
        
    def create(self, user_id: int, product: Product) -> Product:
        new_id = max([p.id for p in self.db.products], default=100) + 1

        new_product = Product(
            _id=new_id,
            user_id=user_id,
            product_name=product.product_name,
            age_range=product.age_range,
            ingredients=product.ingredients,
            additive=product.additive,
            nutrition=product.nutrition,
            manufacturer=product.manufacturer,
            mfg_date=product.mfg_date,
            expiry_date=product.expiry_date,
            net_weight=product.net_weight,
            allergen=product.allergen,
            warning=product.warning,
            origin=product.origin,
            createdAt=utc_now,
            timeZone="Asia/Ho_Chi_Minh",
            createdAtLocal=utc_now.astimezone(ZoneInfo("Asia/Ho_Chi_Minh"))
        )

        self.db.products.append(new_product)
        return new_product

    def get_products_by_date(
        self,
        user_id: int,
        day: int,
        month: int,
        year: int
    ) -> list[Product]:
        return [
            product
            for product in self.db.products
            if product.user_id == user_id
            and product.createdAtLocal.day == day
            and product.createdAtLocal.month == month
            and product.createdAtLocal.year == year
        ]
