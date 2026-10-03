from src.core.product.exceptions import ProductAlreadyExistsError, ProductNotFoundError


class ProductManager:
    def __init__(self):
        self.products = {}

    def add(self, product):
        if self._validate_product(product.id):
            raise ProductAlreadyExistsError("product already exists")
        self.products[product.id] = product

    def get(self, product_id):
        if not self._validate_product(product_id):
            raise ProductNotFoundError("product not found")
        return self.products[product_id]

    def update(self, product_id, product):
        if not self._validate_product(product_id):
            raise ProductNotFoundError("product not found")
        self.products[product_id] = product

    def delete(self, product_id):
        if not self._validate_product(product_id):
            raise ProductNotFoundError("product not found")
        del self.products[product_id]

    def _validate_product(self, product_id):
        return product_id in self.products

product_manager = ProductManager()
