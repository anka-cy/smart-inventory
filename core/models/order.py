from datetime import datetime
from core.models.customer import Customer
from core.models.product import Product
from core.models.order_item import OrderItem
from core.exceptions.base import InvalidQuantityException


class Order:
    def __init__(self, id, customer: Customer):
        self.id = id
        self.customer = customer
        self.order_date = datetime.now()
        self.items = []

    def add_item(self, product: Product, quantity: int):
        if quantity <= 0:
            raise InvalidQuantityException("Quantity must be greater than zero")

        item = OrderItem(product, quantity)
        self.items.append(item)

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item.get_subtotal()
        return total
