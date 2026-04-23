import mysql.connector
import os


def get_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),        # endpoint de AWS RDS
            user=os.getenv("DB_USER"),        # usuario MySQL
            password=os.getenv("DB_PASSWORD"),# contraseña
            database=os.getenv("DB_NAME"),    # nombre de la base de datos
            port=3306
        )
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return connection