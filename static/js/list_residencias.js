// Obtener el modal
var modal = document.getElementById("addResidenciaModal");

// Obtener el botón que abre el modal
var addBtn = document.getElementById("addResidenciaBtn");

// Obtener el elemento <span> que cierra el modal
var span = document.getElementsByClassName("close")[0];

// Cuando el usuario hace clic en el botón, abre el modal
addBtn.onclick = function() {
    document.getElementById("modalTitle").innerText = "Agregar Nueva Residencia";
    document.getElementById("submitBtn").innerText = "Agregar Residencia";
    document.getElementById("residenciaForm").reset();
    document.getElementById("residenciaId").value = "";
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

// Manejar la edición de una residencia
var editBtns = document.getElementsByClassName("editResidenciaBtn");
for (var i = 0; i < editBtns.length; i++) {
    editBtns[i].onclick = function() {
        var residenciaId = this.getAttribute("data-id");
        fetch(`/get_residencia/${residenciaId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById("modalTitle").innerText = "Editar Residencia";
                document.getElementById("submitBtn").innerText = "Editar Residencia";
                document.getElementById("residenciaId").value = residenciaId;
                document.getElementById("id_nombre").value = data.nombre;
                document.getElementById("id_cantidad_apartamentos").value = data.cantidad_apartamentos;
                document.getElementById("id_jefe_consejo").value = data.jefe_consejo;
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

// Manejar la eliminación de una residencia
var deleteBtns = document.getElementsByClassName("deleteResidenciaBtn");
for (var i = 0; i < deleteBtns.length; i++) {
    deleteBtns[i].onclick = function() {
        var residenciaId = this.getAttribute("data-id");
        if (confirm("¿Estás seguro de que deseas eliminar esta residencia?")) {
            fetch(`/delete_residencia/${residenciaId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Error al eliminar la residencia.");
                }
            });
        }
    }
}
