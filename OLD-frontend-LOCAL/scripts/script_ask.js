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

    try {
        const PreguntasUsuario = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ pregunta })
        });
    } catch (error) {
        console.error("Error al enviar la pregunta:", error);
    }

    // Hacer scroll al final otra vez por si la respuesta es larga
    chatWindow.scrollTop = chatWindow.scrollHeight;
});

// Botón de bajar al final
const scrollToBottomBtn = document.createElement("button");
scrollToBottomBtn.id = "scroll-to-bottom-btn";
scrollToBottomBtn.textContent = "↓";
scrollToBottomBtn.style.display = "none";
scrollToBottomBtn.style.position = "fixed";
scrollToBottomBtn.style.right = "36px";
scrollToBottomBtn.style.bottom = "100px";
scrollToBottomBtn.style.zIndex = "30";
scrollToBottomBtn.style.background = "#e0f2e9";
scrollToBottomBtn.style.color = "#133b21";
scrollToBottomBtn.style.border = "none";
scrollToBottomBtn.style.borderRadius = "50%";
scrollToBottomBtn.style.width = "48px";
scrollToBottomBtn.style.height = "48px";
scrollToBottomBtn.style.fontSize = "2rem";
scrollToBottomBtn.style.boxShadow = "0 2px 8px rgba(34,139,56,0.15)";
scrollToBottomBtn.style.cursor = "pointer";
scrollToBottomBtn.style.transition = "background 0.2s, box-shadow 0.2s";
scrollToBottomBtn.style.alignItems = "center";
scrollToBottomBtn.style.justifyContent = "center";
scrollToBottomBtn.style.display = "flex";
scrollToBottomBtn.style.paddingBottom = "20px";
document.body.appendChild(scrollToBottomBtn);

scrollToBottomBtn.addEventListener("click", () => {
    chatWindow.scrollTop = chatWindow.scrollHeight;
});

function checkScrollBtnVisibility() {
    const threshold = 60;
    if (chatWindow.scrollHeight - chatWindow.scrollTop - chatWindow.clientHeight > threshold) {
        scrollToBottomBtn.style.display = "flex";
    } else {
        scrollToBottomBtn.style.display = "none";
    }
}

chatWindow.addEventListener("scroll", checkScrollBtnVisibility);

function scrollToBottomAndHideBtn() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
    scrollToBottomBtn.style.display = "none";
}

