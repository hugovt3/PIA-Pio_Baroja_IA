const form = document.getElementById("preguntar-form");
const chatWindow = document.getElementById("chat-window");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const preguntaInput = document.getElementById("pregunta");
    const pregunta = preguntaInput.value.trim();
    if (!pregunta) return;

    // Crear y añadir el mensaje del usuario
    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "message user-message";
    userMessageDiv.innerHTML = `<div class="message-content">${pregunta}</div>`;
    chatWindow.appendChild(userMessageDiv);

    // Limpiar el input
    preguntaInput.value = "";

    // Crear y añadir un mensaje de carga para la IA
    const iaMessageDiv = document.createElement("div");
    iaMessageDiv.className = "message pia-message";
    iaMessageDiv.innerHTML = `<div class="message-content">Pensando...</div>`;
    chatWindow.appendChild(iaMessageDiv);

    // Hacer scroll al final
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        const respuesta = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ pregunta })
        });
        const data = await respuesta.json();
        iaMessageDiv.querySelector(".message-content").textContent = data.respuesta;
    } catch (error) {
        iaMessageDiv.querySelector(".message-content").textContent = "Error al obtener respuesta.";
    }

    // Hacer scroll al final otra vez por si la respuesta es larga
    chatWindow.scrollTop = chatWindow.scrollHeight;
});

