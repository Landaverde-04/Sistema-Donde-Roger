



//metodo para mostrar el modal de confirmacion de habilitar proveedor
document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalConfirmarHabilitar');
  const nombreSpan = document.getElementById('modalNombreProveedorHabilitar');
  const btnHabilitar = document.getElementById('btnHabilitarProveedor');
  modal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const proveedorId = button.getAttribute('data-id');
    const proveedorNombre = button.getAttribute('data-nombre');
    nombreSpan.textContent = proveedorNombre;
    btnHabilitar.href = `/Proveedor/habilitar/${proveedorId}/`;
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