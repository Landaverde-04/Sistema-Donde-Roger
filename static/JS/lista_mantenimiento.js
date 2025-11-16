document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalConfirmarEliminar');
  const nombreSpan = document.getElementById('modalNombreMantenimiento');
  const btnEliminar = document.getElementById('btnEliminarMantenimiento');

  modal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const mantenimientoId = button.getAttribute('data-id');
    const mantenimientoNombre = button.getAttribute('data-nombre');

    // Actualiza el nombre en el texto del modal
    nombreSpan.textContent = mantenimientoNombre;

    // Establece el enlace de eliminación
    btnEliminar.href = `/mantenimientos/${mantenimientoId}/eliminar/`;
  });
});
