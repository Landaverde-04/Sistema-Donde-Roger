document.addEventListener('DOMContentLoaded', function() {
  // Modal eliminar
  var modalEliminar = document.getElementById('modalEliminar');
  if (modalEliminar) {
    modalEliminar.addEventListener('show.bs.modal', function (event) {
      var button = event.relatedTarget;
      var url = button.getAttribute('data-url');
      var nombreEmpleado = button.getAttribute('data-nombre');
      document.getElementById('modalNombreEmpleado').innerText = nombreEmpleado;
      var btnEliminarEmpleado = document.getElementById('btnEliminarEmpleado');
      btnEliminarEmpleado.href = url;
    });
  }
});