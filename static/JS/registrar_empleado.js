// Mostrar el modal de éxito si exito=1 en la URL
function mostrarModal(mensaje) {
  document.getElementById('modalMensajeTexto').textContent = mensaje;
  const modal = new bootstrap.Modal(document.getElementById('mensajeModal'));
  modal.show();
}

window.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("exito") === "1") {
    mostrarModal("¡Empleado registrado exitosamente!");
  }
});
