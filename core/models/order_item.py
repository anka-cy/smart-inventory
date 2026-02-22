from core.models.product import Product
from core.exceptions.base import InvalidQuantityException


class OrderItem:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise InvalidQuantityException("Quantity must be greater than zero")
        self.product = product
        self.quantity = quantity

    def get_subtotal(self):
        return self.product.price * self.quantity
