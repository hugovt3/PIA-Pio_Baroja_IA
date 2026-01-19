const form = document.getElementById("preguntar-form");
const responseDiv = document.getElementById("respuesta");

form.addEventListener("submit", async (e) => {
    e.preventDefault(); // hace que no se cambie la pagina al enviar el formulario

    const pregunta = document.getElementById("pregunta").value;
    responseDiv.innerHTML = "Loading...";

    const respuesta = await fetch("/ask", { //con await asegura que espere la respuesta y de tiempo al servidor y a la IA a pensar la respuesta
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ pregunta }) //aqui enviamos el JSON al backend
    });

    const data = await respuesta.json();
    responseDiv.innerHTML = data.respuesta; //aqui cogemos la parte de JSON que tiene la respuesta y se la enseñamos al usuario
});