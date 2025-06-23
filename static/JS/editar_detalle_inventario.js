
//se asignan eventos a los botones
document.getElementById("btnNuevafila").addEventListener("click", addRow);
agregarEventosBotonesEliminarActuales();

//Se baso en la funcion de crear, con el cambio que los campos de name tienen el prefijo de nuevo.
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
    inputCantidad.id = "nuevo-cantidad-" + row.rowIndex;
    inputCantidad.name = "nuevo-cantidad-" + row.rowIndex;
    inputCantidad.setAttribute("min", "0");
    inputCantidad.required = true;

    const inputIngreso = ingreso.appendChild(document.createElement("input"));
    inputIngreso.classList.add("form-control");
    inputIngreso.type = "datetime-local";
    inputIngreso.value = result;
    inputIngreso.id = "nuevo-ingreso-" + row.rowIndex;
    inputIngreso.name = "nuevo-ingreso-" + row.rowIndex;
    inputIngreso.required = true;

    const inputCaducidad = caducidad.appendChild(document.createElement("input"));
    inputCaducidad.classList.add("form-control");
    inputCaducidad.type = "date";
    inputCaducidad.id = "nuevo-caducidad-" + row.rowIndex;
    inputCaducidad.name = "nuevo-caducidad-" + row.rowIndex;
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
    const filasPrecargadas = tbody.querySelectorAll('[id^="anterior-fila-"],[id^="actual-fila-"]');
    const ultimaPrecargada = filasPrecargadas[filasPrecargadas.length - 1];
    for (let i = ultimaPrecargada.rowIndex ; i < rows.length; i++) {
        const indice = rows[i].rowIndex;
        const cantidad = rows[i].querySelectorAll('[id^="nuevo-cantidad-"]');
        const ingreso = rows[i].querySelectorAll('[id^="nuevo-ingreso-"]');
        const caducidad = rows[i].querySelectorAll('[id^="nuevo-caducidad-"]');
        const eliminar = rows[i].querySelectorAll('[id^="eliminar-"]');
        cantidad[0].id = "nuevo-cantidad-" + indice;
        cantidad[0].name = "nuevo-cantidad-" + indice;
        ingreso[0].id = "nuevo-ingreso-" + indice;
        ingreso[0].name = "nuevo-ingreso-" + indice;
        caducidad[0].id = "nuevo-caducidad-" + indice;
        caducidad[0].name = "nuevo-caducidad-" + indice;
        eliminar[0].id = "eliminar-" + indice;
        eliminar[0].name = "eliminar-" + indice;
        rows[i].id = "fila-" + indice;
    }

}
//Esta funcion agrega los onclick respectivos a los botones de los detalles precargados
function agregarEventosBotonesEliminarActuales(){
    const tbody = document.getElementById("tabla-cantidades").getElementsByTagName("tbody")[0];
    const filasActuales = tbody.querySelectorAll('[id^="actual-fila-"]');
    for (let i = 0; i < filasActuales.length; i++) {
        const btnEliminar = filasActuales[i].querySelectorAll('[id^="eliminar-actual-"]');
        btnEliminar[0].onclick = function () {
            eliminarFila(filasActuales[i]);
        }
    }
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