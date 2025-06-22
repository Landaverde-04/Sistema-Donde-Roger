document.addEventListener('DOMContentLoaded', function() {
  // Modal eliminar usuario: configura el link con el id correcto
  var modalEliminar = document.getElementById('modalConfirmarEliminar');
  if (modalEliminar) {
    modalEliminar.addEventListener('show.bs.modal', function (event) {
      var button = event.relatedTarget;
      var idUsuario = button.getAttribute('data-id');
      var nombreUsuario = button.getAttribute('data-nombre');
      document.getElementById('modalNombreUsuario').innerText = nombreUsuario;
      var btnEliminar = document.getElementById('btnEliminarUsuario');
      btnEliminar.href = "/usuarios/eliminar/" + idUsuario + "/"; // Modifica la ruta si es diferente
    });
  }
  // Modal de éxito desde Django messages
  var mensajeExito = document.getElementById('mensajeExito');
  if (mensajeExito && mensajeExito.value) {
    var modal = new bootstrap.Modal(document.getElementById('mensajeModal'));
    document.getElementById('modalMensajeTexto').innerText = mensajeExito.value;
    modal.show();
  }
});