import mysql.connector
from mysql.connector import Error
from database.dao.db_config import DB_CONFIG

class BaseDAO:
    def __init__(self):
        db_settings = DB_CONFIG

        self.db_config = {
            'user': db_settings['USER'],
            'password': db_settings['PASSWORD'],
            'host': db_settings['HOST'],
            'port': db_settings.get('PORT'),
            'database': db_settings['NAME']
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise e
