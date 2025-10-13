function agregarDireccion() {
    // Crear un nuevo elemento textarea
    const contenedor = document.getElementById('direcciones');
    const ultimo = contenedor.querySelector('.direccion:last-of-type') || contenedor.lastElementChild;
    const cantidad = contenedor.querySelectorAll('.direccion').length + 1;

         const html = `
            <div class="campo full" id="div-direccion${cantidad}">
            <label>Dirección adicional:</label>            
            <textarea id='direccion${cantidad}' name="direccion_cliente" rows="1" cols="80"></textarea>
            <button type="button" class="btn btn-danger" onclick="this.parentElement.remove()">Eliminar</button>
            </div>
        `;
        
        if(ultimo) {
            ultimo.insertAdjacentHTML('afterend', html);
        } else {
            contenedor.insertAdjacentHTML('beforeend', html);
        }

        const nuevoTextarea = document.getElementById(`direccion${cantidad}`);
        if (nuevoTextarea) {
            nuevoTextarea.focus();
        }

        document.addEventListener('DOMContentLoaded', () => {
            const contenedor = document.getElementById('direcciones');
            if (!contenedor) return;

            contenedor.addEventListener('click', (event) => {
                if (event.target.classlist.contains('btn-danger')) {
                    const bloque = event.target.closest('.direccion');
                    if (bloque) {
                        bloque.remove();
                        renumerar(contenedor)
                    }
                }
            });
        });
    
}