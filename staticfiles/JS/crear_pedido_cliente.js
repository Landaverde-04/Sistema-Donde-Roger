const botonesProductos = document.querySelectorAll('button[id^="add"]');
const form = document.getElementById('form-crear-pedido');
const rbtnTipos = document.querySelectorAll('input[id^="tipo"]');
const switchAsociar = document.getElementById('asociar');
const modalSeleccionCliente = document.getElementById('modal-seleccion-cliente');
const modalSeleccionClienteBody = document.getElementById('modal-seleccion-cliente-body');
const tablaModalSeleccionCliente = document.getElementById('modal-seleccion-tabla');
const inputModalSeleccionClienteBuscar = document.getElementById('modal-seleccion-cliente-buscar');
const btnTriggerSeleccionCliente = document.getElementById('btn-seleccionar-cliente');
const btnSeleccionarCliente = document.getElementById('modal-cliente-seleccionar');
const addNuevaDireccion = document.getElementById('chk-nuevo-direccion');
const btnEliminarCliente = document.getElementById('btn-eliminar-cliente');
const btnGuardarCliente = document.getElementById('modal-crear-cliente-guardar');
const modalCrearCliente = bootstrap.Modal.getOrCreateInstance(document.getElementById('modal-crear-cliente'));
const formClienteNuevo = document.getElementById('form-cliente-nuevo');
let filaSeleccionada = null;
var botonesSubstract = document.querySelectorAll('button[id^="sub"]');
var botonesBorrar = document.querySelectorAll('button[id^="remove"]');
var detallesPedido = [];
const tipoSeleccionado = document.querySelector('input[name="inlineRadioOptions"]:checked');
const areaDestino = document.getElementById('destino');
var clienteSeleccionado = {};

// actualizarAreaDestino('tipo1'); ⌦ 

//Evento para evitar que el form se envie vacio, deberia ser con bootstrap pero asi se fue
form.addEventListener('submit', function (event) {
    if (detallesPedido.length === 0) {
        alert('Debe agregar al menos un producto al pedido.');
        event.preventDefault();
        return;
    }
    const detalles = JSON.stringify(detallesPedido);
    document.getElementById('detalles-pedido').value = detalles;

});

//Evento para agregar productos al total del pedido
botonesProductos.forEach(boton => {
    boton.addEventListener('click', function () {
        const idProducto = this.id.trim().split('-')[1];
        agregarProducto(idProducto);
    });
});

//Evento para cambiar los campos segun el tipo de pedido
rbtnTipos.forEach(rbtn => {
    rbtn.addEventListener('change', function () {
        var selected = this.value;
        actualizarAreaDestino(selected);
    });

});

//Evento para asociar un cliente al pedido, habilita los botones correspondientes
switchAsociar.addEventListener('change', function () {
    switchCamposCliente(this.checked);
    const direccionCheck = document.getElementById('chk-direccion');
    const direccionSelect = document.getElementById('direccion');
    const direccionInput = document.getElementById('direccion-nueva');
    if (this.checked) {
        direccionCheck.classList.remove('d-none');
        direccionSelect.classList.remove('d-none');
        direccionInput.classList.add('d-none');
    }
    else {
        direccionCheck.classList.add('d-none');
        direccionSelect.classList.add('d-none');
        direccionInput.classList.remove('d-none');
    }
});

//Evento para buscar los clientes dentro del modal
inputModalSeleccionClienteBuscar.addEventListener('change', buscarCliente);
inputModalSeleccionClienteBuscar.addEventListener('input', buscarCliente);
// btnTriggerSeleccionCliente.addEventListener('click',buscarCliente);

//Evento para para cargar los clientes en la tabla del modal cuando se muestra
modalSeleccionCliente.addEventListener('shown.bs.modal', buscarCliente);

//evento para pre-seleccionar un cliente en la tabla del modal
tablaModalSeleccionCliente.addEventListener('click', (e) => {
    const fila = e.target.closest('tr');
    if (!fila | fila.parentElement.tagName.toLowerCase() === "thead") {
        return;
    }
    if (filaSeleccionada) filaSeleccionada.classList.remove('table-warning', 'fw-bold');
    fila.classList.add('table-warning', 'fw-bold');
    filaSeleccionada = fila;
});

btnSeleccionarCliente.addEventListener('click', async () => {
    const idCliente = filaSeleccionada.id.split('-')[1];
    const cliente = await obtenerCliente(idCliente);
    await seleccionarCliente(cliente);


});

addNuevaDireccion.addEventListener('change', function () {
    const direccionInput = document.getElementById('direccion-nueva');
    const direccionSelect = document.getElementById('direccion');
    if (addNuevaDireccion.checked) {
        direccionSelect.classList.add('d-none');
        direccionInput.classList.remove('d-none');
    }
    else {
        direccionSelect.classList.remove('d-none');
        direccionInput.classList.add('d-none');
    }
});

btnEliminarCliente.addEventListener('click', resetCliente);
btnGuardarCliente.addEventListener('click', async () => {

    if (!formClienteNuevo.checkValidity()) {
        formClienteNuevo.classList.add("was-validated");
        return;
    }
    const nombres = document.getElementById('input-nuevo-cliente-nombres').value;
    const apellidos = document.getElementById('input-nuevo-cliente-apellidos').value;
    const dui = document.getElementById('input-nuevo-cliente-dui').value;
    const telefono = document.getElementById('input-nuevo-cliente-telefono').value;
    const email = document.getElementById('input-nuevo-cliente-email').value;
    const nacimiento = document.getElementById('input-nuevo-cliente-nacimiento').value;
    resetCliente();
    await seleccionarCliente(await agregarCliente(nombres, apellidos, dui, telefono, email, nacimiento));
    modalCrearCliente.hide();
});
// FUNCIONES --------------------

//Funcion para obtener los botones segun se van generando y agregandoles eventos, son los del detalle de pedido
function updateButtons() {
    botonesSubstract = document.querySelectorAll('button[id^="sub"]');
    botonesBorrar = document.querySelectorAll('button[id^="remove"]');

    botonesSubstract.forEach(boton => {
        boton.addEventListener('click', function () {
            const idProducto = this.id.split('-')[1];
            restarProducto(idProducto);
        });
    });

    botonesBorrar.forEach(boton => {
        boton.addEventListener('click', function () {
            const idProducto = this.id.split('-')[1];
            borrarProducto(idProducto);
        });
    });
}





function agregarProducto(idProductoMenu) {
    const atributos = document.getElementById(`producto-${idProductoMenu}`).getElementsByTagName('td');
    const precio = parseFloat(atributos[1].innerText.replace('$', '').trim());
    const existente = detallesPedido.find(d => d.idProductoMenu === idProductoMenu);
    if (existente) {
        existente.cantidadPedido++;
        existente.subtotalPedido += existente.precio;
    }
    else {
        const d = {
            idProductoMenu: idProductoMenu,
            nombreProducto: atributos[0].innerText,
            cantidadPedido: 1,
            precio: precio,
            subtotalPedido: precio,
        };
        detallesPedido.push(d);
    }
    actualizarPedido();
}

function restarProducto(idProductoMenu) {
    const detalle = detallesPedido.find(d => d.idProductoMenu === idProductoMenu);
    if (detalle.cantidadPedido === 1) {
        borrarProducto(idProductoMenu);
    }
    detalle.cantidadPedido--;
    detalle.subtotalPedido -= detalle.precio;
    actualizarPedido();
}

function borrarProducto(idProductoMenu) {
    const index = detallesPedido.findIndex(d => d.idProductoMenu === idProductoMenu);
    detallesPedido.splice(index, 1);
    actualizarPedido();
}

function actualizarPedido() {
    const pedido = document.getElementById('detalle-pedido').getElementsByTagName('tbody')[0];
    const total = document.getElementById('detalle-pedido').getElementsByTagName('tfoot')[0].getElementsByTagName('td')[0];
    pedido.innerHTML = '';
    total.innerHTML = '';
    var sumatoria = 0;
    detallesPedido.forEach(d => {
        sumatoria += d.subtotalPedido;
        pedido.insertRow().innerHTML = `<tr>
            <td>${d.nombreProducto}</td>
            <td>$${d.precio.toFixed(2)}</td>
            <td>
            ${d.cantidadPedido}
            <button id="sub-${d.idProductoMenu}" type="button" class="btn btn-outline-danger btn-sm">-</button>
            </td>
            <td>$${d.subtotalPedido.toFixed(2)}</td>
            <td><button id="remove-${d.idProductoMenu}" type="button" class="btn btn-danger btn-sm"><i class="bi bi-trash"></i></button></td>
        </tr>`;
    });
    total.innerHTML = `$${sumatoria.toFixed(2)}`;
    updateButtons();
}

function actualizarAreaDestino(tipo) {
    const restaurante = document.getElementById('campos-restaurante');
    const clienteRecoger = document.getElementById('campos-recoger');
    const domicilio = document.getElementById('campos-domicilio');

    // SETEAMOS TODOS A OCULTOS Y LO CAMBIAMOS DEPENDIENDO DEL TIPO
    restaurante.classList.add('d-none');
    clienteRecoger.classList.add('d-none');
    domicilio.classList.add('d-none');

    // no se si ya lo tiene lo duplica, veré
    switch (tipo) {
        case '1':
            restaurante.classList.remove('d-none');
            break;
        case '2':
            clienteRecoger.classList.remove('d-none');
            break;
        case '3':
            domicilio.classList.remove('d-none');
            break;
        default:
            restaurante.classList.remove('d-none');
            break;
    }

}

function switchCamposCliente(checked) {
    const camposCliente = document.getElementById('datos-cliente');
    const camposDestino = document.getElementById('datos-entrega');
    if (checked) {
        camposCliente.classList.remove('d-none');
        camposDestino.classList.remove('w-100');
        camposDestino.classList.add('w-50');
    }
    else {
        camposCliente.classList.add('d-none');
        camposDestino.classList.remove('w-50');
        camposDestino.classList.add('w-100');
    }

}

async function obtenerClientes(text, page = 1) {
    try {
        const response = await fetch(
            `/pedidos/api/clientes/?names=${encodeURIComponent(text)}&page=${page}&per_page=5`
        );

        if (!response.ok) throw new Error("Error en la petición al servidor");

        const data = await response.json();
        console.log(data);

        renderTabla(data.results);
        renderPaginacion(data.page, data.total_pages, text);

        ultimaPagina = data.page;
    } catch (error) {
        console.error(error);
        tablaBody.innerHTML = `
            <tr><td colspan="5" class="text-center text-danger">Error cargando datos</td></tr>
        `;
    }
}

async function agregarCliente(nombres, apellidos, dui, telefono, email, nacimiento) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch(
            `/pedidos/api/clientes/`,
            {
                method: 'POST',
                headers: {
                    "X-CSRFToken": csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    nombreCliente: nombres,
                    apellidoCliente: apellidos,
                    duiCliente: dui,
                    telefonoCliente: telefono,
                    emailCliente: email,
                    nacimientoCliente: nacimiento,
                }).toString(),
            }
        );

        if (!response.ok) throw new Error("Error en la petición al servidor");

        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
        return null;
    }
}


async function obtenerCliente(idCliente) {
    try {
        const response = await fetch(
            `/pedidos/api/clientes/?idCliente=${idCliente}`
        );

        if (!response.ok) throw new Error("Error en la petición al servidor");

        const data = await response.json();
        console.log(data.results[0]);
        return data.results[0];
    } catch (error) {
        console.error(error);
        return null;
    }
}

async function obtenerDirecciones(idCliente) {
    try {
        const response = await fetch(
            `/pedidos/api/clientes/direcciones/?idCliente=${idCliente}`
        );

        if (!response.ok) throw new Error("Error en la petición al servidor");

        const data = await response.json();
        console.log(data.results);
        return data.results;
    }
    catch (error) {
        console.error(error);
        return null;
    }
}

/* ===============================
   RENDER TABLA
================================= */

function renderTabla(clientes) {
    const tablaBody = modalSeleccionClienteBody.querySelector("tbody");
    tablaBody.innerHTML = "";

    if (!clientes.length) {
        const row = tablaBody.insertRow();
        const cell = row.insertCell();
        cell.colSpan = 5;
        cell.textContent = "No hay clientes registrados";
        cell.classList.add("text-center", "text-muted");
        return;
    }

    clientes.forEach(cliente => {
        const row = tablaBody.insertRow();
        row.id = "fila-" + cliente.idCliente;

        row.insertCell(0).textContent = cliente.nombreCliente + " " + cliente.apellidoCliente;
        row.insertCell(1).textContent = cliente.duiCliente;
        row.insertCell(2).textContent = cliente.telefonoCliente;
        row.insertCell(3).textContent = cliente.emailCliente;
        row.insertCell(4).textContent = cliente.nacimientoCliente;
    });
}

/* ===============================
   RENDER PAGINACION
================================= */

function renderPaginacion(current, total, ultimaBusqueda) {
    const paginacion = document.getElementById("pagination-container");
    paginacion.innerHTML = "";
    var ultimoTextoBuscado = ultimaBusqueda;
    if (total <= 1) return;

    let html = `<div class="btn-group">`;

    if (current > 1) {
        html += `
            <button class="btn btn-outline-secondary"
                    onclick="obtenerClientes('${ultimoTextoBuscado}', ${current - 1})">
                « Anterior
            </button>`;
    }

    for (let i = 1; i <= total; i++) {
        html += `
            <button class="btn btn-${i === current ? "secondary" : "outline-secondary"}"
                    onclick="obtenerClientes('${ultimoTextoBuscado}', ${i})">
                ${i}
            </button>`;
    }

    if (current < total) {
        html += `
            <button class="btn btn-outline-secondary"
                    onclick="obtenerClientes('${ultimoTextoBuscado}', ${current + 1})">
                Siguiente »
            </button>`;
    }

    html += `</div>`;
    paginacion.innerHTML = html;
}


function buscarCliente() {
    var busqueda = inputModalSeleccionClienteBuscar.value.toLowerCase();
    var criterios = [];
    if (busqueda.length > 3) {
        criterios[0] = busqueda;
    }
    obtenerClientes(criterios[0]);
}

async function seleccionarCliente(idCliente) {
    const cardCliente = document.getElementById(`cliente-selected`);
    const idClienteSeleccionado = document.getElementById('idCliente');
    if (idCliente) {
        cardCliente.classList.remove('d-none');
        const nombreCliente = document.getElementById(`nombre-cliente-selected`);
        const telefonoCliente = document.getElementById(`telefono-cliente-selected`);
        const emailCliente = document.getElementById(`email-cliente-selected`);
        const nacimientoCliente = document.getElementById(`nacimiento-cliente-selected`);
        idClienteSeleccionado.value = idCliente.idCliente;
        nombreCliente.innerHTML = `<i class="bi bi-person-fill"></i>` + " " + idCliente.nombreCliente + " " + idCliente.apellidoCliente;
        telefonoCliente.innerText = "Telefono: " + idCliente.telefonoCliente;
        emailCliente.innerText = "Email: " + idCliente.emailCliente;
        nacimientoCliente.innerText = "Nacimiento: " + idCliente.nacimientoCliente;

        const direcciones = await obtenerDirecciones(idCliente.idCliente);
        const select = document.getElementById('direccion');
        select.innerHTML = "";
        direcciones.forEach(direccion => {
            const option = document.createElement('option');
            option.value = direccion.direccion;
            option.innerText = direccion.direccion;
            select.appendChild(option);
        });
    }
    else {
        cardCliente.classList.add('d-none');
    }
}

function resetCliente() {
    const cardCliente = document.getElementById(`cliente-selected`);
    const select = document.getElementById('direccion');
    select.innerHTML = `<option value="" selected disabled>Seleccione un cliente</option>`;
    cardCliente.classList.add('d-none');
    const idClienteSeleccionado = document.getElementById('idCliente');
    idClienteSeleccionado.value = null;
}

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()