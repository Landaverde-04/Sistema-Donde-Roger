const botonesProductos = document.querySelectorAll('button[id^="add"]');
const form = document.getElementById('form-crear-pedido');
const rbtnTipos = document.querySelectorAll('input[id^="tipo"]');
const switchAsociar = document.getElementById('asociar');
var botonesSubstract = document.querySelectorAll('button[id^="sub"]');
var botonesBorrar = document.querySelectorAll('button[id^="remove"]');
var detallesPedido = [];
const tipoSeleccionado = document.querySelector('input[name="inlineRadioOptions"]:checked');
const areaDestino = document.getElementById('destino');
// actualizarAreaDestino('tipo1'); ⌦ 


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
        const idProducto = this.id.trim().split('-')[1];
        agregarProducto(idProducto);
    });
});

rbtnTipos.forEach(rbtn => { 
    rbtn.addEventListener('change', function () {
        var selected = this.value;
        actualizarAreaDestino(selected);
    });

});

switchAsociar.addEventListener('change', function () {
    switchCamposCliente(this.checked);
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

function switchCamposCliente(checked){
    const camposCliente = document.getElementById('datos-cliente');
    const camposDestino = document.getElementById('datos-entrega');
    if(checked){
        camposCliente.classList.remove('d-none');
        camposDestino.classList.remove('w-100');
        camposDestino.classList.add('w-50');
    }
    else{
        camposCliente.classList.add('d-none');
        camposDestino.classList.remove('w-50');
        camposDestino.classList.add('w-100');
    }

}