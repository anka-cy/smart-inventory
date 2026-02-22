from database.dao.base_dao import BaseDAO
from core.models.product import Product


class ProductDAO(BaseDAO):
    def save(self, product: Product):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO products (name, category, price, quantity_in_stock) VALUES (%s, %s, %s, %s)"
            values = (product.name, product.category, product.price, product.quantity_in_stock)
            cursor.execute(query, values)
            conn.commit()
            product.id = cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def update(self, product: Product):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE products SET name=%s, category=%s, price=%s, quantity_in_stock=%s WHERE id=%s"
            values = (product.name, product.category, product.price, product.quantity_in_stock, product.id)
            cursor.execute(query, values)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self, product_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "DELETE FROM products WHERE id=%s"
            cursor.execute(query, (product_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def find_by_id(self, product_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT id, name, category, price, quantity_in_stock FROM products WHERE id=%s"
            cursor.execute(query, (product_id,))
            row = cursor.fetchone() 

            if row:
                return Product(row[0], row[1], row[2], float(row[3]), row[4])
            return None
        finally:
            cursor.close()
            conn.close()
