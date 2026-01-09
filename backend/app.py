from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "PIA backend funcionando correctamente 🚀"

@app.route("/test-ollama")
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

if __name__ == "__main__":
    app.run(debug=True)
