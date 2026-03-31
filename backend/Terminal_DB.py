from Conexion_DB import get_connection #Importar el metodo para conetarse a la BBDD y poder reutilizar la misma conexión

Conexion = get_connection()
Conexion_cursor = Conexion.cursor()
indice = 1

#CONSULTA PARA EDITAR LA BBDD
Conexion_cursor.execute("DELETE FROM documents")
Conexion_cursor.execute("DELETE FROM chunks ")
Conexion_cursor.execute("DELETE FROM sqlite_sequence")
 


Conexion.commit()
Conexion.close()
