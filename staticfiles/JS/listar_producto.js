document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form-producto');
    if (form) {
        form.addEventListener('submit', function(event) {
            let nombre = document.getElementById('nombre').value.trim();
            let unidad = document.getElementById('unidadMedida').value.trim();
            let marca = document.getElementById('marcaProducto').value.trim();
            let errores = [];
            if (!nombre) errores.push("El nombre es obligatorio.");
            if (!unidad) errores.push("La unidad de medida es obligatoria.");
            if (!marca) errores.push("La marca es obligatoria.");
            if (errores.length > 0) {
                alert(errores.join('\n'));
                event.preventDefault();
            }
        });
    }
});