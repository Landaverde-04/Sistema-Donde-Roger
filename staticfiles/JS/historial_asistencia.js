document.addEventListener('DOMContentLoaded', () => {
  const inputNombre = document.getElementById('busquedaEmpleado');
  const inputFecha = document.getElementById('busquedaFecha');
  const filas = document.querySelectorAll('#tablaAsistencias tbody tr');

  function filtrarTabla() {
    const nombre = inputNombre.value.toLowerCase();
    const fecha = inputFecha.value;

    filas.forEach(fila => {
      const nombreEmpleado = fila.querySelector('.col-nombre').innerText.toLowerCase();
const fechaAsistencia = fila.querySelector('.col-fecha').getAttribute('data-fecha');


      const coincideNombre = nombreEmpleado.includes(nombre);
      const coincideFecha = fecha ? fechaAsistencia === fecha : true;

      fila.style.display = (coincideNombre && coincideFecha) ? '' : 'none';
    });
  }

  inputNombre.addEventListener('input', filtrarTabla);
  inputFecha.addEventListener('input', filtrarTabla);
});
