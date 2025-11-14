document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalConfirmarEliminar');
  const nombreSpan = document.getElementById('modalNombreMaquinaria');
  const btnEliminar = document.getElementById('btnEliminarMaquinaria');

  modal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const maquinariaId = button.getAttribute('data-id');
    const maquinariaNombre = button.getAttribute('data-nombre');

    // Actualiza el nombre en el texto del modal
    nombreSpan.textContent = maquinariaNombre;

    // Establece el enlace de eliminación
    btnEliminar.href = `/maquinaria/${maquinariaId}/eliminar/`;
  });
});
