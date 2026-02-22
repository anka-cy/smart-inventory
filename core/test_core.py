from core.models.product import Product
from core.models.customer import Customer
from core.models.order import Order
from core.exceptions.base import  OutOfStockException, InvalidEmailException

def test():
    print("---  core Tests ---")

    print("\n[Step 1] Product Logic")
    try:
        p = Product(101, "Wireless Mouse", "Electronics", 25.50, 50)
        
        if p.name != "Wireless Mouse":
            print("  [Error] Product name is wrong!")
        elif p.quantity_in_stock != 50:
            print("  [Error] Product stock is wrong!")
        else:
            print("  [OK] Product 'Wireless Mouse' created successfully")
        
        p.add_stock(10)
        if p.quantity_in_stock == 60:
            print("  [OK] Stock increased to 60")
        else:
            print(f"  [Error] Stock check failed! Expected 60, got {p.quantity_in_stock}")
            
        p.remove_stock(5)
        if p.quantity_in_stock == 55:
            print("  [OK] Stock decreased to 55")
        else:
            print(f"  [Error] Stock check failed! Expected 55, got {p.quantity_in_stock}")
            
    except Exception as e:
        print(f"  [Error] Product test crashed: {e}")

    print("\n[Step 2] Validation & Errors")
    try:
        try:
            Product(999, "Error Item", "Test", -1.0, 10)
            print("  [Error] System accepted a negative price!")
        except ValueError:
            print("  [OK] Correctly blocked negative price")

        try:
            p.remove_stock(100)
            print("  [Error] System allowed removing more stock than available!")
        except OutOfStockException:
            print("  [OK] Correctly blocked over-removal of stock")
            
    except Exception as e:
        print(f"  [Error] Error check crashed: {e}")

    print("\n[Step 3] Customer Logic")
    try:
        c = Customer(1, "ahmed howari", "ahmed.m@provider.com")
        if c.email == "ahmed.m@provider.com":
            print(f"  [OK] Customer '{c.name}' created with valid email")
        else:
            print("  [Error] Customer email was not saved correctly")
            
        try:
            Customer(2, "Test User", "not_an_email")
            print("  [Error] System accepted an invalid email!")
        except InvalidEmailException:
            print("  [OK] Correctly blocked malformed email")
            
    except Exception as e:
        print(f"  [Error] Customer test crashed: {e}")

    print("\n[Step 4] Order Calculations")
    try:
        buyer = Customer(50, "Sara bennani", "sarabennani.j@email.com")
        desk = Product(201, "Wooden Desk", "Furniture", 150.0, 5)
        lamp = Product(202, "Table Lamp", "Furniture", 30.0, 20)
        
        sale = Order(1001, buyer)
        sale.add_item(desk, 1)
        sale.add_item(lamp, 2)
        
        grand_total = sale.calculate_total()
        if grand_total == 210.0:
            print(f"  [OK] Grand total is perfect: ${grand_total}")
        else:
            print(f"  [Error] Total mismatch! Expected 210.0, got {grand_total}")
            
    except Exception as e:
        print(f"  [Critical] Order test crashed: {e}")

    print("\n--- All tests finished! ---")

if __name__ == "__main__":
    test()
