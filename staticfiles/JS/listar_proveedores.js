//metodo para mostrar mensaje de exito al registrar proveedor
function mostrarModal(mensaje) {
  document.getElementById('modalMensajeTexto').textContent = mensaje;
  const modal = new bootstrap.Modal(document.getElementById('mensajeModal'));
  modal.show();
}
//metodo para modificar el modal a la hora de editar proveedor mensaje de exito
function mostrarModalEditar(mensaje, titulo="") {
  document.getElementById('modalMensajeTexto').textContent = mensaje;
  document.getElementById('mensajeModalLabel').textContent = titulo;
  const modal = new bootstrap.Modal(document.getElementById('mensajeModal'));
  modal.show();
}
//metodo que manda a llamar el modal en caso el proveedor haya sido registrado exitosamente
window.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("exito") === "1") {
    mostrarModal("¡Proveedor registrado exitosamente!");    
  }else if (params.get("exito") === "2") {
    mostrarModalEditar("¡Proveedor editado exitosamente!", "Edicion exitosa");
    };
})
  

document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalConfirmarEliminar');
  const nombreSpan = document.getElementById('modalNombreProveedor');
  const btnEliminar = document.getElementById('btnEliminarProveedor');

  modal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const proveedorId = button.getAttribute('data-id');
    const proveedorNombre = button.getAttribute('data-nombre');

    // Actualiza el nombre en el texto del modal
    nombreSpan.textContent = proveedorNombre;

    // Establece el enlace de eliminación
    btnEliminar.href = `/Proveedor/deshabilitar/${proveedorId}`;
  });
});

//funcion para hacer busqueda en proveedores
document.addEventListener('DOMContentLoaded', () => {
  const inputNombre = document.getElementById('busquedaProveedor');  
  const filas = document.querySelectorAll('#tablaProveedores tbody tr');

  function filtrarTabla() {
    const nombre = inputNombre.value.toLowerCase();    

    filas.forEach(fila => {
      const nombreProveedor = fila.querySelector('.col-nombre').innerText.toLowerCase();
      const apellidoProveedor = fila.querySelector('.col-apellido').innerText.toLowerCase();
      const empresaProveedor = fila.querySelector('.col-empresa').innerText.toLowerCase();

      const coincideNombre = nombreProveedor.includes(nombre);
      

      fila.style.display = (coincideNombre) || apellidoProveedor.includes(nombre) || empresaProveedor.includes(nombre) ? '' : 'none';
    });
  }

  inputNombre.addEventListener('input', filtrarTabla);  
});