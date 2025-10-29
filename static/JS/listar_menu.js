
    $(document).ready(function () {
        const inputBuscar = document.getElementById("inputBuscar"); //Obtener el input de busqueda
        const selectCategoria = document.getElementById("selectCategoria"); //Obtener el select de categoria
        const btnLimpiar = document.getElementById("btnLimpiar"); //Obtener el boton de limpieza
        btnLimpiar.addEventListener("click", limpiarBusqueda);
        inputBuscar.addEventListener("change", buscarProducto);
        selectCategoria.addEventListener("change", buscarProducto);
    });
    function buscarProducto() {
        var busqueda = inputBuscar.value.toLowerCase();
        var categoria = selectCategoria.value;
        var criterios = [];
        if (selectCategoria.selectedIndex !== 0){
                criterios[1] = categoria;
            }
        if (busqueda.length > 0) {
            criterios[0] = busqueda;
        }
        obtenerProductos(criterios[0], criterios[1]);
    }

    function limpiarBusqueda() {
        inputBuscar.value = "";
        selectCategoria.selectedIndex = 0;
        buscarProducto();
    }

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
                    acciones.innerHTML = `<a href="/menu/ver/${producto.idProductoMenu}" class="btn btn-info">Ver</a>
                    <a href="/menu/editar/${producto.idProductoMenu}" class="btn btn-primary">Editar</a>`;
                 
                }
                )

            }
        })

    }