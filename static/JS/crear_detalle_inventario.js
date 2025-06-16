document.getElementById("btnNuevafila").addEventListener("click", addRow);

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
    inputCantidad.type="number";
    inputCantidad.id = "cantidad-" + row.rowIndex;
    inputCantidad.setAttribute("min", "0");

    const inputIngreso = ingreso.appendChild(document.createElement("input"));
    inputIngreso.classList.add("form-control");
    inputIngreso.type = "datetime-local";
    inputIngreso.id = "ingreso-" + row.rowIndex;

    const inputCaducidad = caducidad.appendChild(document.createElement("input"));
    inputCaducidad.classList.add("form-control");
    inputCaducidad.type = "date";
    inputCaducidad.id = "caducidad-" + row.rowIndex;

    //insertar el boton eliminar
    const botonEliminar = document.createElement("button");
    botonEliminar.classList.add("btn", "btn-danger");
    botonEliminar.type ="button";
    botonEliminar.id = "eliminar-" + row.rowIndex;
    botonEliminar.innerText = "Eliminar";
    botonEliminar.onclick = function(){
        row.remove();
    }
    eliminar.appendChild(botonEliminar);
}
