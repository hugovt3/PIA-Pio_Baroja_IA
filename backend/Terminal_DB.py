from Conexion_DB import get_connection #Importar el metodo para conetarse a la BBDD y poder reutilizar la misma conexión

Conexion = get_connection()
Conexion_cursor = Conexion.cursor()
indice = 1

#CONSULTA PARA EDITAR LA BBDD
#Conexion_cursor.execute("DELETE FROM documents WHERE filename = 'PDF_NBA.pdf'")
#Conexion_cursor.execute("DELETE FROM chunks WHERE ID = 1")
#Conexion_cursor.execute("DELETE FROM sqlite_sequence")
Conexion_cursor.execute("SELECT chunk_text FROM chunks WHERE id = ?", (indice,))# Consulta para obtener el texto del chunk
resultado = Conexion_cursor.fetchone() 
print(resultado)

Conexion.commit()
Conexion.close()
print("Registro X correctamente")