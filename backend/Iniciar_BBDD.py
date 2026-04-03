import sqlite3
import os

def inicializar_bd():
    Ruta_BBDD = os.path.join(os.path.dirname(__file__), "../data/data.db")

    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(Ruta_BBDD), exist_ok=True)

    conexion = sqlite3.connect(Ruta_BBDD)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        chunk_text TEXT, 
        chunk_vector BLOB, 
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos lista")