document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get('exito') === '1') {
    const modal = new bootstrap.Modal(document.getElementById('modal-exito'));
    modal.show();
  }

  setTimeout(() => {
      modal.dismmiss();
    }, 3000);
});