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
    except:
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

        grouped = df.groupby('name')['quantity'].sum().sort_values(ascending=False).head(limit)
        
        results = []
        for name, qty in grouped.items():
            results.append({'name': name, 'quantity': qty})
        return results
    except:
        return []


def get_stock_value():
    try:
        engine = get_db_engine()
        query = "SELECT price, quantity_in_stock FROM products"
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            return 0.0

        val = (df['price'] * df['quantity_in_stock']).sum()
        return float(val)
    except:
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
        avg = df.groupby('order_id')['subtotal'].sum().mean()
        return float(avg)
    except:
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

        monthly_data = df.groupby('month')['subtotal'].sum()
        
        final_list = []
        for m, total in monthly_data.items():
            final_list.append({'month': m, 'subtotal': total})
        return final_list
    except:
        return []


def get_customer_frequency():
    try:
        engine = get_db_engine()
        query = "SELECT customer_id FROM orders"
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            return {'average': 0.0, 'top_customers': []}

        avg_freq = float(df['customer_id'].value_counts().mean())


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

        top_list = []
        for i in range(len(df_top)):
            row = df_top.iloc[i]
            top_list.append({
                'name': row['name'],
                'order_count': int(row['order_count'])
            })

        return {
            'average': avg_freq,
            'top_customers': top_list
        }
    except:
        return {'average': 0.0, 'top_customers': []}
