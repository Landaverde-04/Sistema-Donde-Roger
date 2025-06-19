//metodo para mostrar mensaje de exito al registrar proveedor
function mostrarModal(mensaje) {
  document.getElementById('modalMensajeTexto').textContent = mensaje;
  const modal = new bootstrap.Modal(document.getElementById('mensajeModal'));
  modal.show();
}

window.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("exito") === "1") {
    mostrarModal("¡Proveedor registrado exitosamente!");
  }
});

//metodo para cancelar registro
  document.addEventListener('DOMContentLoaded', function () {
    var btnCancelar = document.getElementById('btnCancelar');
    var myModal = new bootstrap.Modal(document.getElementById('modalCancelar'));

    btnCancelar.addEventListener('click', function (event) {
      event.preventDefault();  // Evita navegación
      myModal.show();          // Muestra el modal
    });
  });
//metodo que agrega fila a la tabla producto
function agregarFila() {
    const tabla = document.querySelector("#tabla-productos tbody");
    const filas = tabla.querySelectorAll("tr");
    const ultimaFila = filas[filas.length - 1];
    const nuevaFila = ultimaFila.cloneNode(true);

    // Limpiar los valores de los inputs
    nuevaFila.querySelectorAll("input").forEach(input => input.value = "");

    tabla.appendChild(nuevaFila);
}

//metodo para eliminar una fila de producto a excepcion de la primera
function eliminarFila(boton) {
    const fila = boton.closest("tr");
    const tabla = document.querySelector("#tabla-productos tbody");
    const filas = tabla.querySelectorAll("tr");

    if (fila === filas[0]) {
        mostrarModal("¡No puedes eliminar la primera fila!");
        return;
    }

    fila.remove();
}
//metodo para validar checkbox que seleccione al menos 1
document.addEventListener("DOMContentLoaded", function () {
  const formulario = document.getElementById("form-proveedor");
  
  formulario.addEventListener("submit", function (e) {
    const checkboxes = document.querySelectorAll("input[name='dias']");
    let alMenosUnoMarcado = false;

    checkboxes.forEach((checkbox) => {
      if (checkbox.checked) {
        alMenosUnoMarcado = true;
      }
    });

    if (!alMenosUnoMarcado) {
      e.preventDefault(); // Evita que el formulario se envíe
      mostrarModal("Debe seleccionar al menos un día de atención.");
    }
  });
});
