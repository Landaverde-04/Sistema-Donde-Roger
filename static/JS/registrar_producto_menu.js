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
            destruirListadoCategorias();
            return;
        }
      }
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