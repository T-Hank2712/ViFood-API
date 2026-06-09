"""
Product Service V0
Trả dữ liệu mock mặc định cho production ổn định.
"""

from typing import List
from app.models.product import Product
from app.repositories.product_repo import ProductRepository

from app.db import db


class ProductServiceV0:

    def __init__(self):
        self.product_repo = ProductRepository(db)
    
    def get_all(self, user_id: int) -> List[Product]:
        """Lấy danh sách products theo user"""
        return self.product_repo.get_all(user_id)

    def get_by_id(self, product_id: int, user_id: int) -> Product | None:
        """Lấy product theo id nhưng phải thuộc user"""
        return self.product_repo.get_by_id(product_id, user_id)

    def count(self, user_id: int) -> int:
        """Đếm products theo user"""
        return self.product_repo.count(user_id)
    
    def create_product(self, user_id: int, product: Product) -> Product:
        """Tạo mới product (giả định)"""
        return self.product_repo.create(user_id=user_id, product=product)

    def get_products_by_date(
        self,
        user_id: int,
        day: int,
        month: int,
        year: int
    ) -> list[Product]:
        return self.product_repo.get_products_by_date(user_id, day, month, year)
    
    def count_by_date(self, user_id: int, day: int, month: int, year: int) -> int:
        return self.product_repo.count_by_date(user_id, day, month, year)
