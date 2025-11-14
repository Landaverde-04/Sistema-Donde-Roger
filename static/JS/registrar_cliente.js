function agregarDireccion() {
  const contenedor = document.getElementById('direcciones');
  const cantidad = contenedor.querySelectorAll('.direccion').length + 1;

  const html = `
    <div class="direccion campo full" id="div-direccion${cantidad}">
      <label>Dirección adicional:</label>
      <textarea id="direccion${cantidad}" name="direccion_cliente" rows="1" cols="80"></textarea>
      <button type="button" class="btn btn-danger btn-eliminar">Eliminar</button>
    </div>
  `;

  contenedor.insertAdjacentHTML('beforeend', html);

  const nuevoTextarea = document.getElementById(`direccion${cantidad}`);
  if (nuevoTextarea) nuevoTextarea.focus();
}

// Delegación de eventos (UNA vez, no dentro de la función)
document.addEventListener('DOMContentLoaded', () => {
  const contenedor = document.getElementById('direcciones');
  if (!contenedor) return;

  contenedor.addEventListener('click', (event) => {
    if (event.target.classList.contains('btn-eliminar')) {
      const bloque = event.target.closest('.direccion');
      if (bloque) {
        bloque.remove();
        renumerarDirecciones(contenedor); // opcional
      }
    }
  });
});

// (Opcional) Renumerar ids/labels si te interesa mantener correlativo
function renumerarDirecciones(contenedor) {
  const bloques = contenedor.querySelectorAll('.direccion');
  let i = 1;
  bloques.forEach((b) => {
    b.id = `div-direccion${i}`;
    const label = b.querySelector('label');
    if (label) label.textContent = i <= 2 ? `Dirección ${i}:` : 'Dirección adicional:';
    const textarea = b.querySelector('textarea[name="direccion_cliente"]');
    if (textarea) {
      textarea.id = `direccion${i}`;
    }
    i++;
  });
}
  document.addEventListener('DOMContentLoaded', function () {
    var btnCancelar = document.getElementById('btnCancelar');
    var myModal = new bootstrap.Modal(document.getElementById('modalCancelar'));

    btnCancelar.addEventListener('click', function (event) {
      event.preventDefault();  // Evita navegación
      myModal.show();          // Muestra el modal
    });
  });