document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".form-busqueda");
    const input = document.getElementById("busquedaCliente");
    const resultados = document.getElementById("resultados");
    const paginacion = document.getElementById("paginacion");
    const reiniciar = document.getElementById("btn-reiniciar");

    // Búsqueda con submit
    form.addEventListener("submit", function(e) {
        e.preventDefault();
        if(input.value.trim() === '') {
        return;
    }
        
        const q = input.value.trim();
        fetch(`?q=${q}`)
            .then(res => res.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                resultados.innerHTML = doc.getElementById("resultados").innerHTML;
                paginacion.innerHTML = doc.getElementById("paginacion").innerHTML;
            });
    });

    //reiniciar búsqueda

        reiniciar.addEventListener("click", function(e) {

            if(input.value.trim() === '') {
        return;
    }
        e.preventDefault();
        input.value = '';
        fetch(`?`)
            .then(res => res.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                resultados.innerHTML = doc.getElementById("resultados").innerHTML;
                paginacion.innerHTML = doc.getElementById("paginacion").innerHTML;
            });
    });

    // Paginación con clic
    document.addEventListener("click", function(e) {
        const link = e.target.closest(".pagination a");
        if (!link) return;
        e.preventDefault();

        fetch(link.href)
            .then(res => res.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                resultados.innerHTML = doc.getElementById("resultados").innerHTML;
                paginacion.innerHTML = doc.getElementById("paginacion").innerHTML;
            });
    });
});

document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalConfirmarEliminar');
  const nombreSpan = document.getElementById('modalNombreCliente');
  const btnEliminar = document.getElementById('btnEliminarCliente');

  modal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const clienteId = button.getAttribute('data-id');
    const clienteNombre = button.getAttribute('data-nombre');

    // Actualiza el nombre en el texto del modal
    nombreSpan.textContent = clienteNombre;

    // Establece el enlace de eliminación
    btnEliminar.href = `/clientes/deshabilitar/${clienteId}`;
  });
});

//metodo para mostrar mensaje de exito al registrar cliente
function mostrarModal(mensaje) {
  document.getElementById('modalMensajeTexto').textContent = mensaje;
  const modal = new bootstrap.Modal(document.getElementById('mensajeModal'));
  modal.show();
}
//metodo para modificar el modal a la hora de editar cliente mensaje de exito
function mostrarModalEditar(mensaje, titulo="") {
  document.getElementById('modalMensajeTexto').textContent = mensaje;
  document.getElementById('mensajeModalLabel').textContent = titulo;
  const modal = new bootstrap.Modal(document.getElementById('mensajeModal'));
  modal.show();
}
//metodo que manda a llamar el modal en caso el cliente haya sido registrado exitosamente
window.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("exito") === "1") {
    mostrarModal("¡Cliente registrado exitosamente!");    
  }else if (params.get("exito") === "2") {
    mostrarModalEditar("¡Cliente editado exitosamente!", "Edicion exitosa");
    };
})