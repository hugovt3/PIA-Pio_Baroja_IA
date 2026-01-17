import sqlite3
import os

Ruta_BBDD = os.path.join(os.path.dirname(__file__), "../data/data.db")

conexion = sqlite3.connect(Ruta_BBDD) # crear conexion
cursor = conexion.cursor() # crear un cursor para ejecutar comandos SQL

cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    path TEXT,
    uploaded_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    text TEXT,
    page_number INTEGER,
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

conexion.commit()
conexion.close()

print("Base de datos inicializada correctamente")