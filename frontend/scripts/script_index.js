// Script para limpiar el formulario de subida de PDFs

function LimpiarSubida() {
    // Obtener el input de archivo y limpiar su valor
    const PdfsSubidos = document.getElementById("pdfs");
    
    if (PdfsSubidos) {
        PdfsSubidos.value = ""; // Limpia los archivos seleccionados
    }
    else {
        console.error("No se encontró el elemento con id 'pdfs'");
    }
}
