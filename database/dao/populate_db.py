from database.dao.product_dao import ProductDAO
from database.dao.customer_dao import CustomerDAO
from database.dao.order_dao import OrderDAO
from core.models.product import Product
from core.models.customer import Customer
from core.models.order import Order

def populate_sample():
    print("--- Simple Database Population ---")

    product_dao = ProductDAO()
    customer_dao = CustomerDAO()
    order_dao = OrderDAO()

    p1 = Product(None, "Laptop", "Electronics", 1200.00, 10)
    p2 = Product(None, "Coffee Table", "Furniture", 150.00, 5)
    p3 = Product(None, "Pen Pack", "Office Supplies", 5.99, 100)

    print("Adding products...")
    product_dao.save(p1)
    product_dao.save(p2)
    product_dao.save(p3)

    c1 = Customer(None, "John Doe", "john@email.com")
    c2 = Customer(None, "Jane Smith", "jane@email.com")

    print("Adding customers...")
    customer_dao.save(c1)
    customer_dao.save(c2)

    print("Adding sample order...")
    order = Order(None, c1)
    order.add_item(p1, 1)
    order.add_item(p3, 2)
    
    order_dao.save(order)

    print("\nDone! Sample data added successfully.")

if __name__ == "__main__":
    populate_sample()
