document.getElementById("btnNuevafila").addEventListener("click", addRow);
addRow();
// document.querySelector('#btnGuardar').addEventListener('click', crearListadoProductos);
const inputProducto = document.getElementById("product_input")
inputProducto.addEventListener("focus", crearListadoProductos);
inputProducto.addEventListener("focusout", destroyListadoProductos);
inputProducto.addEventListener("focusout", validarProducto);
inputProducto.addEventListener("input", actualizarListadoProductos);

let productos = [];
let listadoFiltrado = [];
obtenerProductos();

function addRow() {
    const form = document.getElementById("form");
    form.classList.remove("was-validated");
    const tbody = document.getElementById("tabla-cantidades").getElementsByTagName("tbody")[0];
    const row = tbody.insertRow();
    row.id = "fila-" + row.rowIndex;
    const cantidad = row.insertCell(0);
    const ingreso = row.insertCell(1);
    const caducidad = row.insertCell(2);
    const eliminar = row.insertCell(3);


    //Recuperar fecha y hora actuales
    const now = new Date();
    const localISOString = now.toISOString(); // UTC
    const offset = now.getTimezoneOffset(); // en minutos

    const localDate = new Date(now.getTime() - offset * 60000); // ajustar al horario local
    const result = localDate.toISOString().slice(0, 16);

    //Creamos los elementos dentro de las celdas
    const inputCantidad = cantidad.appendChild(document.createElement("input"));
    inputCantidad.classList.add("form-control");
    inputCantidad.type = "number";
    inputCantidad.id = "cantidad-" + row.rowIndex;
    inputCantidad.name = "cantidad-" + row.rowIndex;
    inputCantidad.setAttribute("min", "0");
    inputCantidad.required = true;

    const inputIngreso = ingreso.appendChild(document.createElement("input"));
    inputIngreso.classList.add("form-control");
    inputIngreso.type = "datetime-local";
    inputIngreso.value = result;
    inputIngreso.id = "ingreso-" + row.rowIndex;
    inputIngreso.name = "ingreso-" + row.rowIndex;
    inputIngreso.required = true;

    const inputCaducidad = caducidad.appendChild(document.createElement("input"));
    inputCaducidad.classList.add("form-control");
    inputCaducidad.type = "date";
    inputCaducidad.id = "caducidad-" + row.rowIndex;
    inputCaducidad.name = "caducidad-" + row.rowIndex;
    inputCaducidad.required = true;

    //insertar el boton eliminar
    const botonEliminar = document.createElement("button");
    botonEliminar.classList.add("btn", "btn-danger");
    botonEliminar.type = "button";
    botonEliminar.id = "eliminar-" + row.rowIndex;
    botonEliminar.innerText = "Eliminar";
    botonEliminar.onclick = function () {
        eliminarFila(row);
    }
    eliminar.appendChild(botonEliminar);
}


//Funcion para eliminar las filas de la tabla de detalles de inventario: recibe el objeto de fila y la remueve, luego
//busca las filas resultantes y actualiza sus id y nombre
function eliminarFila(fila) {
    fila.remove();
    const tbody = document.getElementById("tabla-cantidades").getElementsByTagName("tbody")[0];
    const rows = tbody.rows;
    for (let i = 0; i < rows.length; i++) {
        const indice = rows[i].rowIndex;
        const cantidad = rows[i].querySelectorAll('[id^="cantidad-"]');
        console.log(cantidad);
        const ingreso = rows[i].querySelectorAll('[id^="ingreso-"]');
        const caducidad = rows[i].querySelectorAll('[id^="caducidad-"]');
        const eliminar = rows[i].querySelectorAll('[id^="eliminar-"]');
        cantidad[0].id = "cantidad-" + indice;
        cantidad[0].name = "cantidad-" + indice;
        ingreso[0].id = "ingreso-" + indice;
        ingreso[0].name = "ingreso-" + indice;
        caducidad[0].id = "caducidad-" + indice;
        caducidad[0].name = "caducidad-" + indice;
        eliminar[0].id = "eliminar-" + indice;
        eliminar[0].name = "eliminar-" + indice;
        rows[i].id = "fila-" + indice;
    }

}

function crearListadoProductos() {
    destroyListadoProductos();
    const container = document.getElementById("productos-container");
    const div = container.appendChild(document.createElement("div"));
    div.classList.add("position-absolute", "list-group");
    div.id = "div-listado";
    div.style.width = inputProducto.offsetWidth + "px";

    if (listadoFiltrado.length == 0) {
        for (producto of productos) {
            const item = div.appendChild(document.createElement("button"));
            item.classList.add("list-group-item");
            item.type = "button";
            item.id = "producto-" + producto.idProducto;
            item.innerText = producto.nombreProducto;
            item.onmousedown = function () {
                console.log(item.id);
                seleccionarProducto(item.id.substring(9));
            }
            listadoFiltrado.push(producto);
        }
    } else if (listadoFiltrado.length > 0) {
        for (producto of listadoFiltrado) {
            const item = div.appendChild(document.createElement("button"));
            item.classList.add("list-group-item");
            item.type = "button";
            item.id = "producto-" + producto.idProducto;
            item.innerText = producto.nombreProducto;
            item.onmousedown = function () {
                console.log(item.id);
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
    const id = document.getElementById("product_id");
    const unidadMedida = document.getElementById("unidad_de_medida");
    const marca = document.getElementById("marca");
    const producto = productos.find(producto => producto.idProducto == idProducto);
    input.value = producto.nombreProducto;
    id.value = producto.idProducto;
    unidadMedida.value = producto.unidadMedida;
    marca.value = producto.marcaProducto;
}

function destroyListadoProductos() {
    const divListado = document.querySelector('#div-listado');
    if (divListado) {
        divListado.remove();
    }
}

//Funcion para validar el producto: no recibe parametros, pero utiliza el inputProducto para obtener el valor
//busca el producto en el listado obtenido y realiza la validacion
function validarProducto() {
    const nomProducto = inputProducto.value.toLowerCase();
    const div = document.getElementById("productos-container");
    const validacion = div.querySelector('#validacion');
    const submit = document.getElementById("btnGuardar");
    submit.disabled = false;
    if (validacion) {
        validacion.remove();
        console.log("Validacion eliminada");
    }

    inputProducto.classList.remove("is-valid", "is-invalid");

    if (nomProducto.length > 0) {
        const producto = productos.find(producto => producto.nombreProducto.toLowerCase() == nomProducto);
        const validacion = div.appendChild(document.createElement("div"));
        validacion.id = "validacion";
        if (!producto) {
            inputProducto.classList.add("is-invalid");
            validacion.classList.add("invalid-feedback");
            validacion.innerText = "Producto no encontrado";
            submit.disabled = true;
            return false;
        }
        else {
            validacion.classList.add("valid-feedback");
            inputProducto.classList.add("is-valid");
            return true;
        }

    }
    else {
        inputProducto.classList.remove("is-valid", "is-invalid", "was-validated");
        return false;
    }

}

//Funcion para obtener los productos del servidor 
async function obtenerProductos() {
    fetch('/inventario/api/productos/')
        .then(response => response.json())
        .then(data => {
            productos = data;
            console.log(productos);
        })
}

// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')



    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    })
})()