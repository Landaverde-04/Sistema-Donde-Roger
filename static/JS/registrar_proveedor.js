//metodo para mostrar mensaje de exito al registrar proveedor
window.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("exito") === "1") {
    alert("¡Proveedor registrado exitosamente!");
  }
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
        alert("¡No puedes eliminar la primera fila!");
        return;
    }

    fila.remove();
}
document.querySelectorAll('input[name="producto_precio[]"]').forEach(input => {
  input.addEventListener('input', () => {
    if (input.value !== '' && Number(input.value) < 0) {
      input.value = '';
      alert('El precio no puede ser negativo');
    }
  });
});

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
      alert("Debe seleccionar al menos un día de atención.");
    }
  });
});
