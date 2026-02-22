from database.dao.base_dao import BaseDAO
from core.models.customer import Customer

class CustomerDAO(BaseDAO):
    def save(self, customer: Customer):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO customers (name, email) VALUES (%s, %s)"
            values = (customer.name, customer.email)
            cursor.execute(query, values)
            conn.commit()
            customer.id = cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def update(self, customer: Customer):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE customers SET name=%s, email=%s WHERE id=%s"
            values = (customer.name, customer.email, customer.id)
            cursor.execute(query, values)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self, customer_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "DELETE FROM customers WHERE id=%s"
            cursor.execute(query, (customer_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def find_by_id(self, customer_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT id, name, email FROM customers WHERE id=%s"
            cursor.execute(query, (customer_id,))
            row = cursor.fetchone()
            if row:
                return Customer(row[0], row[1], row[2])
            return None
        finally:
            cursor.close()
            conn.close()
