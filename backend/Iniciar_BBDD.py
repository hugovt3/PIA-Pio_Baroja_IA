import mysql.connector
import os

def inicializar_bd():
    conexion = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        filename TEXT,
        fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        document_id INT,
        chunk_text TEXT,
        chunk_vector LONGBLOB,
        FOREIGN KEY(document_id) REFERENCES documents(ID)
    )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos lista en AWS RDS")