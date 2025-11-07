const botonesProductos = document.querySelectorAll('button[id^="add"]');
const form = document.getElementById('form-crear-pedido');
var botonesSubstract = document.querySelectorAll('button[id^="sub"]');
var botonesBorrar = document.querySelectorAll('button[id^="remove"]');
var detallesPedido = [];
const tipoSeleccionado = document.querySelector('input[name="inlineRadioOptions"]:checked');
const areaDestino = document.getElementById('destino');



form.addEventListener('submit', function (event) {
    if (detallesPedido.length === 0) {
        alert('Debe agregar al menos un producto al pedido.');
        event.preventDefault();
        return;
    }
    const detalles = JSON.stringify(detallesPedido);
    document.getElementById('detalles-pedido').value = detalles;

});

botonesProductos.forEach(boton => {
    boton.addEventListener('click', function () {
        const idProducto = this.id.split('-')[1];
        agregarProducto(idProducto);
    });
});

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