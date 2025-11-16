const btnGenerarDatosEnvio = document.getElementById('generar-datos-envio');
const btnCopiar = document.getElementById('btn-copiar');

btnGenerarDatosEnvio.addEventListener('click', copiarDatosEnvio);
btnCopiar.addEventListener('click', copiarDatosEnvio);

function copiarDatosEnvio() {
    var textareaDatosEnvio = document.getElementById('textArea-datos-envio');
    textareaDatosEnvio.select();
    navigator.clipboard.writeText(textareaDatosEnvio.value);
    alert('Datos copiados al portapapeles');
}