
$(document).ready(function () {
    const inputBuscar = document.getElementById("inputBuscar"); //Obtener el input de busqueda
    const btnBuscar = document.getElementById("btnBuscar"); //Obtener el boton de busqueda
    btnBuscar.addEventListener("click", buscarProducto);
    function buscarProducto() {
        const busqueda = inputBuscar.value.toLowerCase();
        obtenerProductos(busqueda);
    }
});

function obtenerProductos(nombre = '', categoria = '') {
    $.ajax({
        url: 'api/productos/',
        type: 'GET',
        data: {
            nombre: nombre,
            categoria: categoria
        },
        success: function (response) {
            var tBody = document.querySelector("#tablaProductos tbody");
            $(tBody).empty();
            response.forEach(producto => {
                const row = tBody.insertRow();
                row.id = "fila-" + producto.idProductoMenu;
                const nombre = row.insertCell(0);
                const precio = row.insertCell(1);
                const unidad = row.insertCell(2);
                const descripcion = row.insertCell(3);
                const acciones = row.insertCell(4);

                nombre.innerText = producto.nombreProductoMenu;
                precio.innerText = producto.precioProductoMenu;
                unidad.innerText = producto.tamanioProductoMenu;
                descripcion.innerText = producto.descripcionProductoMenu;
                //acciones.innerHTML =;
            }
            )
            
        }
    })

}