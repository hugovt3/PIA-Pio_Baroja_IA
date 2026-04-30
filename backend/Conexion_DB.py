import mysql.connector
import os

def get_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            # Coge las variables de entorno para la BBDD del archivo run_app.bat
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=3306
        )
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return connection