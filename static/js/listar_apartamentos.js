// Obtener el modal
var modal = document.getElementById("addApartamentoModal");

// Obtener el botón que abre el modal
var addBtn = document.getElementById("addApartamentoBtn");

// Obtener el elemento <span> que cierra el modal
var span = document.getElementsByClassName("close")[0];

// Cuando el usuario hace clic en el botón, abre el modal
addBtn.onclick = function() {
    document.getElementById("modalTitle").innerText = "Agregar Nuevo Apartamento";
    document.getElementById("submitBtn").innerText = "Agregar Apartamento";
    document.getElementById("apartamentoForm").reset();
    document.getElementById("apartamentoId").value = "";
    modal.style.display = "block";
}

// Cuando el usuario hace clic en <span> (x), cierra el modal
span.onclick = function() {
    modal.style.display = "none";
}

// Cuando el usuario hace clic en cualquier lugar fuera del modal, cierra el modal
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Manejar la edición de un apartamento
var editBtns = document.getElementsByClassName("editApartamentoBtn");
for (var i = 0; i < editBtns.length; i++) {
    editBtns[i].onclick = function() {
        var apartamentoId = this.getAttribute("data-id");
        fetch(`/get_apartamento/${apartamentoId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById("modalTitle").innerText = "Editar Apartamento";
                document.getElementById("submitBtn").innerText = "Editar Apartamento";
                document.getElementById("apartamentoId").value = apartamentoId;
                document.getElementById("id_residencia").value = data.residencia;
                document.getElementById("id_numero").value = data.numero;
                document.getElementById("id_cantidad_becados").value = data.cantidad_becados;
                document.getElementById("id_jefe_apto").value = data.jefe_apto;
                document.getElementById("id_profesor_atiende").value = data.profesor_atiende;
                modal.style.display = "block";
            });
    }
}

// Obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Manejar la eliminación de un apartamento
var deleteBtns = document.getElementsByClassName("deleteApartamentoBtn");
for (var i = 0; i < deleteBtns.length; i++) {
    deleteBtns[i].onclick = function() {
        var apartamentoId = this.getAttribute("data-id");
        if (confirm("¿Estás seguro de que deseas eliminar este apartamento?")) {
            fetch(`/delete_apartamento/${apartamentoId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Error al eliminar el apartamento.");
                }
            });
        }
    }
}
