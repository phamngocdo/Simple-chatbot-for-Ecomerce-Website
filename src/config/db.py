from mysql import connector
from mysql.connector import Error
from config import DB_CONFIG

def get_db_connection():
    try:
        conn = connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Connected successfully")
            return conn
    except Error as e:
        print("Can not connect database:", e)
        return None

db = get_db_connection()