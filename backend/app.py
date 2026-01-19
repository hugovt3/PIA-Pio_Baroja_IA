from flask import Flask, jsonify, send_from_directory, request, render_template
import requests
import os
from Conexion_DB import get_connection #Importar el metodo para conetarse a la BBDD y poder reutilizar la misma conexión
import pdfplumber # Importar pdfplumber para el procesamiento de PDFs (a implementar)
from Creador_chunks import crear_chunk # Importar la función para crear chunks de texto
from sentence_transformers import SentenceTransformer #Creador de vectores
import numpy as np #importar numpy para hacer transformaciones en los vectores y que faiss pueda aceptarlos
import faiss #importar faiss para la búsqueda de similitud entre vectores

app = Flask(
        __name__,
        static_folder="../frontend", #Carpeta frontend para acceder a styles, script.js e Images
        static_url_path="", #Cambia la busqueda
        template_folder="../frontend/templates" #cambio de template a frontend/templates carpeta
        )

RUTA_GUARDAR_PDFS_SERVIDOR = os.path.join(os.path.dirname(__file__), "..", "docs")# Ruta absoluta a la carpeta donde se guardarán los PDFs

#--------------------------
#Inicializar FAISS
#--------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')  # Cargar el modelo preentrenado (el trnasformador de oraciones)
faiss_index = faiss.IndexFlatL2(384)
Vectores = True #saber si hay veectores en la base de datos o no

try:
    conexion_inicial_faiss = get_connection()
    conexion_inicial_faiss_cursor = conexion_inicial_faiss.cursor()
    vectores = conexion_inicial_faiss_cursor.execute("SELECT chunk_vector FROM chunks").fetchall()
    
    if vectores:  # Si hay vectores en la BD
        vectores_lista = []
        for fila in vectores:
            vector_array = np.frombuffer(fila[0], dtype='float32')
            vectores_lista.append(vector_array)
        
        faiss_index.add(np.vstack(vectores_lista))  # Mejor que np.array()
        print(f"FAISS cargado con {len(vectores_lista)} vectores")
    else:
        print("No hay vectores en la BD, FAISS inicializado vacío")
        Vectores = False
    
    conexion_inicial_faiss.close()
except Exception as e:
    print(f"Error cargando FAISS: {e}")


#--------------------------
#Pagina para servir el frontend principal
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

        #PASO 2: Analizar documento con pdfplumber
        text = ""
        with pdfplumber.open(save_path) as pdf_documento:
            for pagina in pdf_documento.pages:
                page_text = pagina.extract_text()
                if not page_text:
                    continue

                page_text = page_text.replace("\n", " ")
                page_text = " ".join(page_text.split())  # elimina espacios dobles

                text += page_text + " "

        #PASO 3: Crear chunks asociados a este documento con lo analizado de pdfplumber poniendole yo un limite de caracteres a cada chunk (funcion creada en Creador_chunks.py)
        Chunks = crear_chunk(text)

        #PASO 4: Generar vectores con sentence-transformers para cada chunk de pdfplumber
        
        Chunks_vectores = model.encode(Chunks)  # Generar vectores para los chunks
        #PASO 5: Convertir los vectores a float32 porque sino faiss no lo lee
        Chunks_vectores = np.array(Chunks_vectores).astype('float32')

        #PASO 6: Hacer el insert en la base de datos sobre la tabla chunks con los valores conseguidos en los pasos anteriores
        for chunk, chunk_vector in zip(Chunks, Chunks_vectores):
            Conexion_cursor.execute("""
                INSERT INTO chunks (chunk_text, chunk_vector, document_id) VALUES (?, ?, ?)
                """, (chunk, chunk_vector.tobytes(), Id_document))
        
        #------------------------
        # Guardar en faiss todas los vectores de los chunks
        #------------------------
        faiss_index.add(Chunks_vectores)  # Añadir los vectores de los chunks al índice FAISS

        # Guardar la información en la lista de archivos guardados para usarlos en el template de archivos subidos con exito
        saved_files.append(pdf.filename)

    Conexion.commit() # Guardar cambios en la BBDD
    Conexion.close()  # Cerrar conexion cuando se haya guardado todo en la BBDD
    return render_template("upload_success.html", archivos=saved_files)

#--------------------------
#Ruta de preguntas a ollama
#--------------------------
@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method =="GET":
        return send_from_directory(app.template_folder,"ask.html")
    elif request.method =="POST":
        #1 : Obetener la pregunta del usuario
        pregunta = request.get_json().get("pregunta")
        #2 : Convertir la pregunta en un vector
        pregunta_vector = model.encode([pregunta]).astype('float32')
        #3 : Buscar los chunks más similares en FAISS
        k = 5  # Número de vecinos más cercanos a recuperar
        distancias, indices = faiss_index.search(pregunta_vector, k)
        #4 : Recuperar los textos de los chunks desde la base de datos usando los índices obtenidos
        Conexión = get_connection()
        Conexión_cursor = Conexión.cursor()
        chunks_textos = []
        for indice in indices[0]: #es un array de dos dimensiones por lo que accedemos a la primera posicion que es donde estan los indices
            indice = int(indice) + 1  #pasar a entero para confirmar y sumar 1 porque faiss empieza en 0 y la BBDD en 1
            print(indice)
            Conexión_cursor.execute("SELECT chunk_text FROM chunks WHERE id = ?", (indice,))# Consulta para obtener el texto del chunk
            resultado = Conexión_cursor.fetchone() 
            print(resultado)
            if resultado:
                chunks_textos.append(resultado[0]) #cogemos la primera columna que es chunk_text para pasarle el contexto
        Conexión.close()
        print(chunks_textos)
        #5 : Construir el prompt para Ollama
        contexto ="\n".join(chunks_textos) #construyo el contexto con lo que hemos recuperado de la base de datos para pasarselo a ollama
        print(contexto) #esto es para verlo en la terminal y comprobar si funciona bien todo
        if Vectores ==True or chunks_textos:
            prompt_ollama = f"Usa el siguiente contexto para responder a la pregunta de la mejor manera posible.Te llamas P I A y eres un Asistente para contestar preguntes sobre Pdfs que vienen del siguiente contexto. Contesta unicamente en español\n\nContexto:\n{contexto}\n\nPregunta: {pregunta}\n\nRespuesta:"
        else:
            prompt_ollama = f"Responde a la siguiente pregunta de la mejor manera posible.Te llamas P I A y eres un Asistente para contestar preguntes sobre Pdfs, Contesta unicamente en español, No tienes contexto adicional.\n\nPregunta: {pregunta}\n\nRespuesta:"
        print(prompt_ollama)
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "phi",
            "prompt": prompt_ollama,
            "stream": False
        }
        response = requests.post(url, json=payload)
        data = response.json()
        respuesta_ollama = data.get("response", "").strip()
        return jsonify({
            "respuesta": respuesta_ollama
        })









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