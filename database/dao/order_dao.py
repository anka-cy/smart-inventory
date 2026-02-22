from database.dao.base_dao import BaseDAO
from core.models.order import Order
from core.models.customer import Customer
from core.models.product import Product


class OrderDAO(BaseDAO):
    def save(self, order: Order):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()

            query_order = "INSERT INTO orders (customer_id, order_date) VALUES (%s, %s)"
            values_order = (order.customer.id, order.order_date)
            cursor.execute(query_order, values_order)
            order.id = cursor.lastrowid 

            query_item = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
            query_update_stock = "UPDATE products SET quantity_in_stock = %s WHERE id = %s"
            
            for item in order.items:
                values_item = (order.id, item.product.id, item.quantity)
                cursor.execute(query_item, values_item)
                
                cursor.execute(query_update_stock, (item.product.quantity_in_stock, item.product.id))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def find_by_id(self, order_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                    SELECT o.id, o.order_date, c.id, c.name, c.email
                    FROM orders o
                    JOIN customers c ON o.customer_id = c.id
                    WHERE o.id = %s
                    """
            cursor.execute(query, (order_id,))
            row = cursor.fetchone()
            
            if row:
                customer = Customer(row[2], row[3], row[4])
                order = Order(row[0], customer)
                order.order_date = row[1]

                query_items = """
                    SELECT p.id, p.name, p.category, p.price, p.quantity_in_stock, oi.quantity
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """
                cursor.execute(query_items, (order_id,))
                for item_row in cursor.fetchall():
                    product = Product(item_row[0], item_row[1], item_row[2], float(item_row[3]), item_row[4])
                    order.add_item(product, item_row[5])
                
                return order
            return None
        finally:
            cursor.close()
            conn.close()
