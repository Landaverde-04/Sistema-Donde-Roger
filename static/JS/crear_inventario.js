
//Evento para mostrar el modal de exito
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get('exito') === '1') {
    const modal = new bootstrap.Modal(document.getElementById('modal-exito-1'));
    modal.show();

    // Espera a que el modal se muestre completamente antes de iniciar el timeout
    document.getElementById('modal-exito').addEventListener('shown.bs.modal', () => {
      setTimeout(() => {
        window.location.href = 'crear_inventario';
      }, 1000);
    });
  }
  else if (params.get('exito') === '2') {
    const modal = new bootstrap.Modal(document.getElementById('modal-exito-2'));
    modal.show();

    // Espera a que el modal se muestre completamente antes de iniciar el timeout
    document.getElementById('modal-exito-2').addEventListener('shown.bs.modal', () => {
      setTimeout(() => {
        window.location.href = 'crear_inventario';
      }, 1000);
    });
  }
});

