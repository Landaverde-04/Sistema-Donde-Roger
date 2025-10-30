
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
        if (busqueda.length >= 3) {
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
                categoria: categoria,
                habilitado: "True"
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
                    const modal = row.appendChild(document.createElement("div"));
                    modal.innerHTML = `<!-- Modal para deshabilitar -->
                    <div class="modal fade" id="modal-deshabilitar-${producto.idProductoMenu}" tabindex="-1" aria-labelledby="¿Está seguro?"
                        aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered ">
                            <div class="modal-content">
                                <div class="modal-header bg-danger text-white">
                                    <h5 class="modal-title" id="modal-cancelar-titulo">ADVERTENCIA</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                        aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <p>¿Está seguro de que desea deshabilitar del menu el producto <strong>${producto.nombreProductoMenu}</strong> ?</p>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-success" data-bs-dismiss="modal">No</button>
                                    <form method="POST" action="{% url 'deshabilitar_producto_menu' ${producto.idProductoMenu} %}">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-danger">Si</a>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>`;

                    nombre.innerText = producto.nombreProductoMenu;
                    precio.innerText = producto.precioProductoMenu;
                    unidad.innerText = producto.tamanioProductoMenu;
                    descripcion.innerText = producto.descripcionProductoMenu;
                    acciones.innerHTML = `<a href="/Menu/ver_producto_menu/${producto.idProductoMenu}" class="btn btn-primary">Ver</a>
                    <a href="/Menu/editar_producto_menu/${producto.idProductoMenu}" class="btn btn-warning">Editar</a>
                    <button type="button" class="btn btn-danger" data-bs-toggle="modal"
                            data-bs-target="#modal-deshabilitar-${producto.idProductoMenu}">Deshabilitar</button>`;
                 
                }
                )

            }
        })

    }