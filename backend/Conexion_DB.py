import sqlite3
import os

Ruta_BBDD = os.path.join(os.path.dirname(__file__), "../data/data.db")

def get_connection():
    return sqlite3.connect(Ruta_BBDD)