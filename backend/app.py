from flask import Flask, jsonify, send_from_directory, request, render_template
import requests
import os
from Conexion_DB import get_connection #Importar el metodo para conetarse a la BBDD y poder reutilizar la misma conexión
from pdfplumber import PDF # Importar pdfplumber para el procesamiento de PDFs (a implementar)

app = Flask(
        __name__,
        static_folder="../frontend", #Carpeta frontend para acceder a styles, script.js e Images
        static_url_path="", #Cambia la busqueda
        template_folder="../frontend/templates" #cambio de template a frontend/templates carpeta
        )

RUTA_GUARDAR_PDFS_SERVIDOR = os.path.join(os.path.dirname(__file__), "..", "docs")# Ruta absoluta a la carpeta donde se guardarán los PDFs


#--------------------------
#Pagina para servir el frontend
#--------------------------
@app.route("/")
def home():
    return send_from_directory(app.template_folder, "index.html")

#--------------------------
#Ruta para subir los archivos PDF a la carpeta doscs y a la base de datos
#-------------------------- 
@app.route("/upload", methods=["POST"])
def upload_pdfs():
    # request.files.getlist permite recibir varios archivos
    pdf_files = request.files.getlist("pdfs")

    #VARIABLE PARA GUARDAR NOMBRES DE ARCHIVOS SUBIDOS
    saved_files = []

    #VARIABLES DE CONEXION A LA BBDD
    Conexion = get_connection()  # Abrir conexion antes del bucle     
    Conexion_cursor = Conexion.cursor()

    for pdf in pdf_files:
        # Evitamos archivos vacíos
        if pdf.filename == "":
            continue

        # Construimos la ruta final donde se guardará el PDF
        save_path = os.path.join(RUTA_GUARDAR_PDFS_SERVIDOR, pdf.filename)

        # Guardamos el archivo en el servidor
        pdf.save(save_path)

        # Insertar información del archivo en la base de datos TABLA DE DOCUMENTS
        Conexion_cursor.execute("""
            INSERT INTO documents (filename) VALUES (?)
        """, (pdf.filename,))

        #------------------------
        # Insertar en la tabla chunks se hará después del procesamiento del PDF
        #------------------------

        #PASO 1: Conseguir el ID del documento insertado en documents
        Id_document = Conexion_cursor.lastrowid  
        #PASO 2: Crear chunks asociados a este documento con pdfplumber
        
        #PASO 3: Generar vectores con sentence-transformers para cada chunk de pdfplumber
        #PASO 4: Hacer el insert en la base de datos sobre la tabla chunks con los valores conseguidos en los pasos anteriores
        
        #Conexion_cursor.execute("""
        #    INSERT INTO chunks (document_id), (chunk_text), (chunk_vector) VALUES (?), (?) , (?)
        #""", (Id_document), None, None)
        

        # Guardar la información del archivo en la base de datos
        saved_files.append(pdf.filename)

    Conexion.commit() # Guardar cambios en la BBDD
    Conexion.close()  # Cerrar conexion cuando se haya guardado todo en la BBDD
    return render_template("upload_success.html", archivos=saved_files)

#--------------------------
#Ruta de preguntas a ollama (Proceso en desarrollo)
#-------------------------- 
"""@app.route("/ask",methods=["POST"])
def ask
"""






#--------------------------
#Pagina prueba de ollama
#--------------------------
@app.route("/test-ollama") #test de ollama
def test_ollama():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "phi",
        "prompt": (
            "Responde exactamente con esta frase, sin añadir nada más:\n"
            "Ollama funciona correctamente."
        ),
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    data = response.json()

    return jsonify({
        "respuesta_ollama": data.get("response", "").strip()
    })

if __name__ == "__main__": # Inicio app
    app.run(debug=True)
