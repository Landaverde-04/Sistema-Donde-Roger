document.addEventListener("DOMContentLoaded", function() {
  const contenedor = document.getElementById("direcciones");
  const btnAgregar = document.getElementById("agregarDireccion");

  // Modal
  const modal = document.getElementById("modalConfirmarEliminarDireccion");
  const modalTexto = document.getElementById("modalTextoDireccion");
  const btnConfirmarEliminar = document.getElementById("btnConfirmarEliminarDireccion");
  const modalInstance = new bootstrap.Modal(modal);

  let direccionAEliminar = null;

  // Delegación de eventos para botones "Eliminar"
  contenedor.addEventListener("click", function(event) {
    if (event.target.classList.contains("eliminar-direccion")) {
      const button = event.target;
      const texto = button.getAttribute("data-texto");
      direccionAEliminar = button.closest(".direccion");
      modalTexto.textContent = texto;
      modalInstance.show();
    }
  });

  // Confirmar eliminación en el modal
  btnConfirmarEliminar.addEventListener("click", function() {
    if (direccionAEliminar) {
      // Si quieres marcar para eliminar en la BD:
      const inputEliminar = direccionAEliminar.querySelector(".direccion-eliminar");
      if (inputEliminar) inputEliminar.value = "1";

      // Eliminar del HTML
      direccionAEliminar.remove();
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
      <input type="text" name="direccion_texto" class="form-control me-2" value="">
      <button type="button" class="btn btn-danger btn-sm eliminar-direccion" data-id="" data-texto="(Nueva dirección)">
        Eliminar
      </button>
    `;
    contenedor.appendChild(div);
  });
});
