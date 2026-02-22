import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings


def get_db_engine():
    db_settings = settings.DATABASES['default']
    user = db_settings['USER']
    password = db_settings['PASSWORD']
    host = db_settings['HOST']
    port = db_settings.get('PORT')
    name = db_settings['NAME']

    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{name}"
    return create_engine(connection_string)


def get_total_revenue():
    try:
        engine = get_db_engine()
        query = """
                SELECT oi.quantity, p.price
                FROM order_items oi
                         JOIN products p ON oi.product_id = p.id \
                """
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            return 0.0

        df['subtotal'] = df['quantity'] * df['price']
        return float(df['subtotal'].sum())
    except Exception as e:
        print(f"Error calculating revenue: {e}")
        return 0.0


def get_best_selling_products(limit=5):
    try:
        engine = get_db_engine()
        query = """
                SELECT p.name, oi.quantity
                FROM order_items oi
                         JOIN products p ON oi.product_id = p.id \
                """
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            return []

        best_sellers = df.groupby('name')['quantity'].sum().sort_values(ascending=False).head(limit)
        return best_sellers.reset_index().to_dict('records')
    except Exception as e:
        print(f"Error fetching best sellers: {e}")
        return []


def get_stock_value():
    try:
        engine = get_db_engine()
        query = "SELECT price, quantity_in_stock FROM products"
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            return 0.0

        return float((df['price'] * df['quantity_in_stock']).sum())
    except Exception as e:
        print(f"Error fetching stock value: {e}")
        return 0.0


def get_avg_order_value():
    try:
        engine = get_db_engine()
        query = """
                SELECT oi.order_id, oi.quantity, p.price
                FROM order_items oi
                         JOIN products p ON oi.product_id = p.id \
                """
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            return 0.0

        df['subtotal'] = df['quantity'] * df['price']
        return float(df.groupby('order_id')['subtotal'].sum().mean())
    except Exception as e:
        print(f"Error fetching avg order value: {e}")
        return 0.0


def get_monthly_revenue():
    try:
        engine = get_db_engine()
        query = """
                SELECT o.order_date, oi.quantity, p.price
                FROM order_items oi
                         JOIN products p ON oi.product_id = p.id
                         JOIN orders o ON oi.order_id = o.id \
                """
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            return []

        df['order_date'] = pd.to_datetime(df['order_date'])
        df['month'] = df['order_date'].dt.strftime('%Y-%m')
        df['subtotal'] = df['quantity'] * df['price']

        monthly = df.groupby('month')['subtotal'].sum().reset_index()
        return monthly.to_dict('records')
    except Exception as e:
        print(f"Error fetching monthly revenue: {e}")
        return []


def get_customer_frequency():
    try:
        engine = get_db_engine()
        query = "SELECT customer_id FROM orders"
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            return {'average': 0.0, 'top_customers': []}

        counts = df['customer_id'].value_counts()
        avg_freq = float(counts.mean())


        query_names = """
                      SELECT c.name, COUNT(o.id) as order_count
                      FROM orders o
                               JOIN customers c ON o.customer_id = c.id
                      GROUP BY c.id, c.name
                      ORDER BY order_count DESC
                      LIMIT 5 \
                      """
        with engine.connect() as conn:
            df_top = pd.read_sql(query_names, conn)

        top_customers = df_top.to_dict('records')

        return {
            'average': avg_freq,
            'top_customers': top_customers
        }
    except Exception as e:
        print(f"Error fetching customer frequency: {e}")
        return {'average': 0.0, 'top_customers': []}
