from core.models.product import Product
from core.models.customer import Customer
from core.models.order import Order
from core.exceptions.base import OutOfStockException, InvalidEmailException, InvalidQuantityException

def test():
    print("---  core Tests ---")

    try:
        p = Product(101, "Clavier Logitech K120", "Electronics", 89.90, 34)

        if p.name != "Clavier Logitech K120":
            print("  [Error] Product name is wrong!")
        elif p.quantity_in_stock != 34:
            print("  [Error] Product stock is wrong!")
        else:
            print("  [OK] Product 'Clavier Logitech K120' created successfully")

        p.add_stock(10)
        if p.quantity_in_stock == 44:
            print("  [OK] Stock increased to 44")
        else:
            print(f"  [Error] Stock check failed! Expected 44, got {p.quantity_in_stock}")

        p.remove_stock(5)
        if p.quantity_in_stock == 39:
            print("  [OK] Stock decreased to 39")
        else:
            print(f"  [Error] Stock check failed! Expected 39, got {p.quantity_in_stock}")

        value = p.get_value_in_stock()
        expected_value = 89.90 * 39
        if value == expected_value:
            print(f"  [OK] Stock value is correct: ${value:.2f}")
        else:
            print(f"  [Error] Stock value wrong! Expected {expected_value:.2f}, got {value:.2f}")

    except Exception as e:
        print(f"  [Error] Product test crashed: {e}")

    try:
        try:
            Product(999, "truc", "Test", -1.0, 10)
            print("  [Error] System accepted a negative price!")
        except ValueError:
            print("  [OK] Correctly blocked negative price")

        try:
            p.remove_stock(100)
            print("  [Error] System allowed removing more stock than available!")
        except OutOfStockException:
            print("  [OK] Correctly blocked over-removal of stock")

        try:
            Product(800, "test produit", "Test", 10.0, -5)
            print("  [Error] System accepted a negative initial stock!")
        except InvalidQuantityException:
            print("  [OK] Correctly blocked negative initial quantity")

        try:
            p.add_stock(0)
            print("  [Error] System accepted adding zero stock!")
        except InvalidQuantityException:
            print("  [OK] Correctly blocked adding zero stock")

        try:
            p.remove_stock(0)
            print("  [Error] System accepted removing zero stock!")
        except InvalidQuantityException:
            print("  [OK] Correctly blocked removing zero stock")

    except Exception as e:
        print(f"  [Error] Error check crashed: {e}")

    try:
        c = Customer(1, "Hamza", "hamza.dev99@gmail.com")
        if c.email == "hamza.dev99@gmail.com":
            print(f"  [OK] Customer '{c.name}' created with valid email")
        else:
            print("  [Error] Customer email was not saved correctly")

        try:
            Customer(2, "Sara L.", "not_an_email")
            print("  [Error] System accepted an invalid email!")
        except InvalidEmailException:
            print("  [OK] Correctly blocked malformed email")

    except Exception as e:
        print(f"  [Error] Customer test crashed: {e}")

    try:
        buyer = Customer(50, "Mehdi", "mehdi_ait@hotmail.com")
        desk = Product(201, "Chaise bureau IKEA", "Furniture", 449.00, 7)
        lamp = Product(202, "Lampe LED", "Furniture", 75.50, 13)

        sale = Order(1001, buyer)
        sale.add_item(desk, 1)
        sale.add_item(lamp, 2)

        grand_total = sale.calculate_total()
        if grand_total == 600.0:
            print(f"  [OK] Grand total is perfect: ${grand_total}")
        else:
            print(f"  [Error] Total mismatch! Expected 600.0, got {grand_total}")

        empty_order = Order(1002, buyer)
        if empty_order.calculate_total() == 0:
            print("  [OK] Empty order total is $0")
        else:
            print(f"  [Error] Empty order total should be 0, got {empty_order.calculate_total()}")

        try:
            bad_order = Order(1003, buyer)
            bad_order.add_item(desk, 0)
            print("  [Error] System accepted zero quantity in order!")
        except InvalidQuantityException:
            print("  [OK] Correctly blocked zero quantity in order item")

        try:
            bad_order2 = Order(1004, buyer)
            bad_order2.add_item(lamp, -3)
            print("  [Error] System accepted negative quantity in order!")
        except InvalidQuantityException:
            print("  [OK] Correctly blocked negative quantity in order item")

    except Exception as e:
        print(f"  [Error] Order test crashed: {e}")

    print("\n--- All tests finished! ---")


if __name__ == "__main__":
    test()
