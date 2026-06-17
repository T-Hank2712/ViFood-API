from app.models.product import Product


class ProductRepository:

    def __init__(self, db):
        self.db = db

    def get_all(self) -> list[Product]:
        return self.db.products

    def create(self, product: Product) -> Product:
        self.db.products.append(product)
        return product
