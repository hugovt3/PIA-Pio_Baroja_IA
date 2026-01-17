import sqlite3
import os

Ruta_BBDD = os.path.join(os.path.dirname(__file__), "../data/data.db")

conexion = sqlite3.connect(Ruta_BBDD) # crear conexion
cursor = conexion.cursor() # crear un cursor para ejecutar comandos SQL

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
    chunk_vector INTEGER, 
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

# chunk_text-> Almacena el vector del chunk para búsquedas vectoriales
# chunk_vector-> Almacena el texto del chunk


conexion.commit()
conexion.close()

print("Base de datos inicializada correctamente")