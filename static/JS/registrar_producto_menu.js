// Se integra dropdown para categoria de producto del menu, referencia tomada de detalle de inventario

//Obtener input de categoria
input_categoria = document.getElementById("input-categoria-producto");


// agregar eventos al input: para el focus e input

input_categoria.addEventListener("focus", crearListadoCategorias);
input_categoria.addEventListener("focusout", destruirListadoCategorias);
// input_categoria.addEventListener("input", actualizarListadoCategorias);

//Lista de categorias preexistentes y lista de filtradas con el input:

let categorias = [];
let categorias_filtradas = [];
obtenerCategorias();

//Llamada al endpoint para obtener las categorias que ya existen
async function obtenerCategorias() {
    fetch('/Menu/api/categorias/')
        .then(response => response.json())
        .then(data => {
            categorias = data;
        })
}

function crearListadoCategorias(){
    //destruir el listado previo por si acaso
    destruirListadoCategorias();

    //crear el contenedor del listado
    const container = document.getElementById("categorias-container");
    const div = container.appendChild(document.createElement("div"));
    div.classList.add("position-absolute", "list-group");
    div.id = "div-listado";
    div.style.width = input_categoria.offsetWidth + "px";

    //Enriquecer el listado filtrado

    if (categorias_filtradas.length == 0) {
        for (categoria of categorias) {
          const item = div.appendChild(document.createElement("button"));
          item.classList.add("list-group-item");
          item.type = "button";
          item.id = "categoria-" + categoria.idCategoriaProductoMenu;
          item.innerText = categoria.nombreCategoriaProductoMenu;
          item.onmousedown = function () {
            seleccionarCategoria(item.id.substring(10));
          }
          categorias_filtradas.push(categoria);
        }
    }
    else if (categorias_filtradas.length > 0) {
        for (categoria of categorias_filtradas) {
          const item = div.appendChild(document.createElement("button"));
          item.classList.add("list-group-item");
          item.type = "button";
          item.id = "categoria-" + categoria.idCategoriaProductoMenu;
          item.innerText = categoria.nombreCategoriaProductoMenu;
          item.onmousedown = function () {
            seleccionarCategoria(item.id.substring(10));
          }
        }
    }



}

function destruirListadoCategorias(){
  const divListado = document.querySelector('#div-listado');
  if (divListado) {
    divListado.remove();
  }
}

function seleccionarCategoria(idCategoria){
    for (categoria of categorias){
        if (categoria.idCategoriaProductoMenu == idCategoria){
            input_categoria.value = categoria.nombreCategoriaProductoMenu;
            // Guardar el ID en el campo oculto
            document.getElementById('categoria-producto').value = categoria.idCategoriaProductoMenu;
            // Marcar como válido
            input_categoria.classList.remove('is-invalid');
            input_categoria.classList.add('is-valid');
            destruirListadoCategorias();
            return;
        }
      }
}

// Validación adicional para el campo de categoría
if (input_categoria) {
    input_categoria.addEventListener('click', function() {
        const hiddenInput = document.getElementById('categoria-producto');
        if (!hiddenInput.value) {
            input_categoria.classList.remove('is-valid');
        }
    });
}

// Validación en tiempo real para nombre
const nombreInput = document.getElementById('nombre-producto');
if (nombreInput) {
    nombreInput.addEventListener('input', function() {
        const valor = this.value.trim();
        if (valor.length >= 3 && valor.length <= 50) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });
}

// Validación en tiempo real para tamaño
const tamanioInput = document.getElementById('tamanio-producto');
if (tamanioInput) {
    tamanioInput.addEventListener('input', function() {
        const valor = this.value.trim();
        if (valor.length >= 2 && valor.length <= 50) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });
}

// Validación en tiempo real para precio
const precioInput = document.getElementById('precio-producto');
if (precioInput) {
    precioInput.addEventListener('input', function() {
        const valor = parseFloat(this.value);
        if (valor > 0 && valor <= 9999.99) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        } else {
            this.classList.remove('is-valid');
            this.classList.add('is-invalid');
        }
    });
}

// JS para validación de formularios de Bootstrap:
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