function agregarDireccion() {
    // Crear un nuevo elemento textarea
    const contenedor = document.getElementById('direcciones');
    const cantidad = contenedor.querySelectorAll('textarea').length + 1;
    const div_direcciones = document.getElementById('div-direccion' + (cantidad - 1));

        div_direcciones.insertAdjacentHTML('afterend', `
            <div class="campo full" id="div-direccion${cantidad}">
            <label>Dirección adicional:</label>            
            <textarea id='direccion${cantidad}' name="direccion_cliente" rows="1" cols="80"></textarea>
            <button type="button" class="btn btn-danger" onclick="this.parentElement.remove()">Eliminar</button>
            </div>
        `);
        contenedor.appendChild(div);
    
}