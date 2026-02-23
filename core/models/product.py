from core.exceptions.base import InvalidQuantityException, OutOfStockException


class Product:
    def __init__(self, id, name, category, price, quantity_in_stock):
        if price < 0:
            raise ValueError("Price cannot be negative")

        if quantity_in_stock < 0:
            raise InvalidQuantityException("Initial quantity must be positive")

        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.quantity_in_stock = quantity_in_stock

    def add_stock(self, qty):
        if qty <= 0:
            raise InvalidQuantityException("Quantity to add must be positive")
        self.quantity_in_stock += qty

    def remove_stock(self, qty):
        if qty <= 0:
            raise InvalidQuantityException("Quantity to remove must be positive")

        if qty > self.quantity_in_stock:
            raise OutOfStockException(f"Not enough stock. Available: {self.quantity_in_stock}")

        self.quantity_in_stock -= qty

    def get_value_in_stock(self):
        return self.price * self.quantity_in_stock