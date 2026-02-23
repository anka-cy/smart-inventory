# Smart Inventory Management System

A Python/Django application for tracking inventory, customers, and orders.

## Project Structure
- `core/`: Business models and analytics logic.
- `database/`: Database schema and DAO classes.
- `web/django_project/`: Django web application.
- `analytics/`: Jupyter notebook for data analysis.

## Setup Instructions

### 1. Requirements
- Python 3.8+
- MySQL Server

### 2. Installation
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Database Setup
 IMPORTANT – Run schema.sql

Before running the app, you MUST initialize the database schema.
The project uses a centralized Python configuration file. Edit the variables in `database/dao/db_config.py` to match your MySQL setup:

```python
DB_CONFIG = {
    'NAME': 'smart_inventory_db',
    'USER': '',  # Your MySQL username
    'PASSWORD': '',  # Your MySQL password
    'HOST': '', # Your MySQL host
    'PORT': '', # Your MySQL port
}
```

Once your database is configured, initialize the tables by running Django migrations:
```bash
cd web/django_project
python manage.py migrate
```

### 4. Running the App
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/`.
