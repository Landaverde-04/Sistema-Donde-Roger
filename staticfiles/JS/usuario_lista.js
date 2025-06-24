document.addEventListener('DOMContentLoaded', function () {
    var modalEliminarUsuario = document.getElementById('modalEliminarUsuario');
    if (modalEliminarUsuario) {
        modalEliminarUsuario.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var url = button.getAttribute('data-url');
            var nombre = button.getAttribute('data-nombre');
            var form = document.getElementById('formEliminarUsuario');
            form.action = url;
            var spanNombre = document.getElementById('modalNombreUsuario');
            spanNombre.textContent = nombre;
        });
    }
});
