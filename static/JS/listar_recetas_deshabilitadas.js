document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('modalConfirmarHabilitar');
  const nombreSpan = document.getElementById('modalNombreReceta');
  const btnHabilitar = document.getElementById('btnHabilitarReceta');

  modal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const recetaId = button.getAttribute('data-id');
    const recetaNombre = button.getAttribute('data-nombre');

    // Actualiza el nombre en el texto del modal
    nombreSpan.textContent = recetaNombre;

    // Establece el enlace de eliminación
    btnHabilitar.href = `/recetas/habilitar_receta/${recetaId}`;
  });
});

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