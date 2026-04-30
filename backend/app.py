from flask import Flask, jsonify, send_from_directory, request, render_template
import requests
import os
from Conexion_DB import get_connection
from Iniciar_BBDD import inicializar_bd
from Creador_chunks import crear_chunk
import pymupdf4llm
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from pathlib import Path

inicializar_bd()

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path="",
    template_folder="../frontend/templates"
)

RUTA_GUARDAR_PDFS_SERVIDOR = os.path.join(os.path.dirname(__file__), "..", "docs")

PREGUNTAS_USUARIO = []
RESPUESTAS_IA = []


# FAISS
model = SentenceTransformer('all-MiniLM-L6-v2')
faiss_index = faiss.IndexFlatL2(384)
Vectores = True

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chunk_vector FROM chunks")
    vectores = cursor.fetchall()

    if vectores:
        vectores_lista = []
        for fila in vectores:
            vector_array = np.frombuffer(fila[0], dtype='float32')
            vectores_lista.append(vector_array)

        faiss_index.add(np.vstack(vectores_lista))
        print(f"FAISS cargado con {len(vectores_lista)} vectores")
    else:
        print("FAISS vacío")
        Vectores = False

    conn.close()
except Exception as e:
    print(f"Error FAISS: {e}")


# RUTAS
@app.route("/")
def welcome():
    return send_from_directory(app.template_folder, "welcome.html")

@app.route("/inicio")
def home():
    return send_from_directory(app.template_folder, "index.html")


# SUBIDA PDFs
@app.route("/upload", methods=["POST"])
def upload_pdfs():
    pdf_files = request.files.getlist("pdfs")
    saved_files = []

    conn = get_connection()
    cursor = conn.cursor()

    for pdf in pdf_files:
        if pdf.filename == "":
            continue

        save_path = os.path.join(RUTA_GUARDAR_PDFS_SERVIDOR, pdf.filename)
        pdf.save(save_path)

        cursor.execute(
            "INSERT INTO documents (filename) VALUES (%s)",
            (pdf.filename,)
        )

        Id_document = cursor.lastrowid

        # PROCESAR PDF
        pdf_path = Path(save_path)

        try:
            md_text = pymupdf4llm.to_markdown(
                pdf_path,
                pages=None,
                hdr_info=True,
                table_strategy="lines_strict",
                write_images=False,
                margins=(50, 50, 50, 50),
            )

            md_text = md_text.replace("\n\n\n", "\n\n")
            md_text = " ".join(md_text.split())
            md_text = md_text.replace(" . ", ". ").strip()

            text = md_text

        except Exception as e:
            print(f"Error pymupdf4llm: {e}")
            text = ""

        # CHUNKS
        chunks = crear_chunk(text)

        vectores = model.encode(chunks)
        vectores = np.array(vectores).astype('float32')

        for chunk, vector in zip(chunks, vectores):
            cursor.execute(
                "INSERT INTO chunks (chunk_text, chunk_vector, document_id) VALUES (%s, %s, %s)",
                (chunk, vector.tobytes(), Id_document)
            )

        faiss_index.add(vectores)
        saved_files.append(pdf.filename)

    conn.commit()
    conn.close()

    return render_template("upload_success.html", archivos=saved_files)


# PREGUNTAS
@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        return send_from_directory(app.template_folder, "ask.html")

    pregunta = request.get_json().get("pregunta")

    pregunta_vector = model.encode([pregunta]).astype('float32')
    distancias, indices = faiss_index.search(pregunta_vector, 5)

    conn = get_connection()
    cursor = conn.cursor()

    chunks_textos = []

    for indice in indices[0]:
        indice = int(indice) + 1

        cursor.execute(
            "SELECT chunk_text FROM chunks WHERE id = %s",
            (indice,)
        )

        resultado = cursor.fetchone()

        if resultado:
            chunks_textos.append(resultado[0])

    conn.close()

    contexto = "\n".join(chunks_textos)

    prompt = f"""
    Responde usando SOLO este contexto:

    {contexto}

    Pregunta:
    {pregunta}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    respuesta = data.get("response", "").strip()

    return jsonify({"respuesta": respuesta})


# MAIN
if __name__ == "__main__":
    app.run(debug=True)