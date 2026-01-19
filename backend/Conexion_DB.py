import sqlite3
import os

Ruta_BBDD = os.path.join(os.path.dirname(__file__), "../data/data.db")

def get_connection():
    Devolucion= None
    try:
        Devolucion= sqlite3.connect(Ruta_BBDD)
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return Devolucion