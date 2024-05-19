import mysql.connector
from mysql.connector import Error


def connect_db():
    db_name = 'library_system'
    user = 'root'
    password = 'Rwbybrown@4547'
    host = 'localhost'

    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )

        cursor = conn.cursor()

        if conn.is_connected():
            print("Connection Established")
            return conn

    except Error as e:
        print(f"Error: {e}")
        return None

