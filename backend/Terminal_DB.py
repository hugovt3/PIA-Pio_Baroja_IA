from Conexion_DB import get_connection #Importar el metodo para conetarse a la BBDD y poder reutilizar la misma conexión

Conexion = get_connection()
Conexion_cursor = Conexion.cursor()

#CONSULTA PARA EDITAR LA BBDD
Conexion_cursor.execute("DELETE FROM documents WHERE filename = 'PDF_NBA.pdf'")



Conexion.commit()
Conexion.close()
print("Registro X correctamente")