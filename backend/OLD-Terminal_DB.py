
#
# OLD - cuando la BBDD era local
#

from Conexion_DB import get_connection #Importar el metodo para conetarse a la BBDD y poder reutilizar la misma conexión

Conexion = get_connection()
Conexion_cursor = Conexion.cursor()
indice = 1

#CONSULTA PARA EDITAR LA BBDD
#Conexion_cursor.execute("DELETE FROM documents where ID != ?", (1,))
#Conexion_cursor.execute("DELETE FROM chunks where ID> ?", (142,))
#Conexion_cursor.execute("DELETE FROM sqlite_sequence")
#Conexion_cursor.execute("INSERT INTO sqlite_sequence (name,seq) VALUES ('documents', ?)", (1,))
#Conexion_cursor.execute("INSERT INTO sqlite_sequence (name,seq) VALUES ('chunks', ?)", (142,))
Conexion_cursor.execute("DELETE FROM chunks where ID> ?", (142,))


Conexion.commit()
Conexion.close()
