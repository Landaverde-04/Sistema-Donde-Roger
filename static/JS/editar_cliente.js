document.addEventListener("DOMContentLoaded", function() {
  const contenedor = document.getElementById("direcciones");
  const btnAgregar = document.getElementById("agregarDireccion");

  // Modal
  const modal = document.getElementById("modalConfirmarEliminarDireccion");
  const btnConfirmarEliminar = document.getElementById("btnConfirmarEliminarDireccion");
  const modalInstance = new bootstrap.Modal(modal);

  let direccionAEliminar = null;

  // Delegación de eventos para botones "Eliminar"
  contenedor.addEventListener("click", function(event) {
    if (event.target.classList.contains("eliminar-direccion")) {
      direccionAEliminar = event.target.closest(".direccion");
      modalInstance.show(); // ya no seteamos texto
    }
  });

  // Confirmar eliminación en el modal
  btnConfirmarEliminar.addEventListener("click", function() {
    if (direccionAEliminar) {
      const inputEliminar = direccionAEliminar.querySelector(".direccion-eliminar");
      if (inputEliminar) inputEliminar.value = "1";

      const txt = direccionAEliminar.querySelector('input[name="direccion_texto"]');
      if (txt) {
        txt.required = false;
        // NO deshabilitar para que se envíe en el formulario
        // txt.disabled = true;
        // txt.value = "";
      }

      const visible = direccionAEliminar.querySelector(".direccion-visible");
      if (visible) visible.classList.add("d-none");

      direccionAEliminar = null;
    }
    modalInstance.hide();
  });

  // Agregar dirección nueva
  btnAgregar.addEventListener("click", () => {
    const div = document.createElement("div");
    div.classList.add("direccion", "mb-2", "d-flex", "align-items-center");
    div.innerHTML = `
      <input type="hidden" name="direccion_id" value="">
      <input type="hidden" name="direccion_eliminar" value="0" class="direccion-eliminar">

      <div class="direccion-visible d-flex align-items-center w-100">
        <input type="text" name="direccion_texto" class="form-control me-2 flex-grow-1" value="" required>
        <button type="button" class="btn btn-danger btn-sm eliminar-direccion">
          Eliminar
        </button>
      </div>
    `;
    contenedor.appendChild(div);
  });

});
  document.addEventListener('DOMContentLoaded', function () {
    var btnCancelar = document.getElementById('btnCancelar');
    var myModal = new bootstrap.Modal(document.getElementById('modalCancelar'));

    btnCancelar.addEventListener('click', function (event) {
      event.preventDefault();  // Evita navegación
      myModal.show();          // Muestra el modal
    });
  });
