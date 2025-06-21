document.getElementById("btnNuevafila").addEventListener("click", addRow);
// document.querySelector('#btnGuardar').addEventListener('click', crearListadoProductos);
const inputProducto = document.getElementById("product_input")
inputProducto.addEventListener("focus", crearListadoProductos);
inputProducto.addEventListener("focusout", destroyListadoProductos);
inputProducto.addEventListener("input", actualizarListadoProductos);

let productos = [];
let listadoFiltrado = [];
obtenerProductos();

function addRow() {
    const tbody = document.getElementById("tabla-cantidades").getElementsByTagName("tbody")[0];
    const row = tbody.insertRow();
    row.id = "fila-" + row.rowIndex;
    const cantidad = row.insertCell(0);
    const ingreso = row.insertCell(1);
    const caducidad = row.insertCell(2);
    const eliminar = row.insertCell(3);


    //Creamos los elementos dentro de las celdas
    const inputCantidad = cantidad.appendChild(document.createElement("input"));
    inputCantidad.classList.add("form-control");
    inputCantidad.type = "number";
    inputCantidad.id = "cantidad-" + row.rowIndex;
    inputCantidad.name = "cantidad-" + row.rowIndex;
    inputCantidad.setAttribute("min", "0");

    const inputIngreso = ingreso.appendChild(document.createElement("input"));
    inputIngreso.classList.add("form-control");
    inputIngreso.type = "datetime-local";
    inputIngreso.id = "ingreso-" + row.rowIndex;
    inputIngreso.name = "ingreso-" + row.rowIndex;

    const inputCaducidad = caducidad.appendChild(document.createElement("input"));
    inputCaducidad.classList.add("form-control");
    inputCaducidad.type = "date";
    inputCaducidad.id = "caducidad-" + row.rowIndex;
    inputCaducidad.name = "caducidad-" + row.rowIndex;

    //insertar el boton eliminar
    const botonEliminar = document.createElement("button");
    botonEliminar.classList.add("btn", "btn-danger");
    botonEliminar.type = "button";
    botonEliminar.id = "eliminar-" + row.rowIndex;
    botonEliminar.innerText = "Eliminar";
    botonEliminar.onclick = function () {
        row.remove();
    }
    eliminar.appendChild(botonEliminar);
}

function crearListadoProductos() {
    destroyListadoProductos();
    const container = document.getElementById("productos-container");
    const div = container.appendChild(document.createElement("div"));
    div.classList.add("position-absolute", "list-group");
    div.id = "div-listado";
    
    if (listadoFiltrado.length == 0) {
        for (producto of productos) {
            const item = div.appendChild(document.createElement("button"));
            item.classList.add("list-group-item");
            item.type = "button";
            item.id = "producto-" + producto.idProducto;
            // const boton = item.appendChild(document.createElement("button"));
            // boton.type = "button";
            // boton.setAttribute("style", "background-color: white; border: none;");
            item.innerText = producto.nombreProducto;
            item.onclick = function () {
                seleccionarProducto(item.id.substring(9));
            }
            listadoFiltrado.push(producto);
        }
    } else if(listadoFiltrado.length > 0) {
        for (producto of listadoFiltrado) {
            const item = div.appendChild(document.createElement("button"));
            item.classList.add("list-group-item");
            item.type = "button";
            item.id = "producto-" + producto.idProducto;
            item.innerText = producto.nombreProducto;
            item.onclick = function () {
                seleccionarProducto(item.id.substring(9));
            }
        }
        
    }
}

function actualizarListadoProductos() {
    const text = inputProducto.value.toLowerCase();
    console.log(text);
    if (text.length > 0) {
        console.log("Productos:");
        console.log(productos);
        listadoFiltrado = [];
        for (producto of productos) {
            const nomProducto = producto.nombreProducto.toLowerCase();
            if (text === nomProducto.substring(0, text.length)) {
                listadoFiltrado.push(producto);
            }
        }
        crearListadoProductos();
    }
    else {
        listadoFiltrado = [];
        crearListadoProductos();

    }
}

function seleccionarProducto(idProducto) {
    const input = document.getElementById("product_input");
    const unidadMedida = document.getElementById("unidad_de_medida");
    const marca = document.getElementById("marca");
    const producto = productos.find(producto => producto.idProducto == idProducto);
    input.value = producto.nombreProducto;
    unidadMedida.value = producto.unidadMedida;
    marca.value = producto.marcaProducto;
}

function destroyListadoProductos() {
    const divListado = document.querySelector('#div-listado');
    if (divListado) {
        divListado.remove();
    }
}


async function obtenerProductos() {
    fetch('/inventario/api/productos/')
        .then(response => response.json())
        .then(data => {
            productos = data;
            console.log(productos);
        })
}
