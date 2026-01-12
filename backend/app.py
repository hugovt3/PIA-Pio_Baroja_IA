from flask import Flask, jsonify, send_from_directory
import requests

app = Flask(
        __name__,
        static_folder="../frontend", #cambio de template a frontend carpeta
        static_url_path="", #Cambia la busqueda
        template_folder="../frontend" #cambio de template a frontend carpeta
        )


@app.route("/") # Ruta de prueba La primera ruta que se accede
def home():
    return send_from_directory(app.template_folder, "index.html")

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
