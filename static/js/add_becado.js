// Obtener el modal
var modal = document.getElementById("addBecadoModal");

// Obtener el botón que abre el modal
var addBtn = document.getElementById("addBecadoBtn");

// Obtener el elemento <span> que cierra el modal
var span = document.getElementsByClassName("close")[0];

// Cuando el usuario hace clic en el botón, abre el modal
addBtn.onclick = function() {
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

document.addEventListener('DOMContentLoaded', () => {
    const editModal = document.getElementById('editBecadoModal');
    const closeEditSpan = document.querySelector('.close-edit');
    const editButtons = document.querySelectorAll('.edit-becado-btn');

    // Abre modal y carga datos
    editButtons.forEach(button => {
        button.addEventListener('click', () => {
            const becadoId = button.getAttribute('data-becado-id');
            fetch(`/get_becado/${becadoId}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('editBecadoId').value = becadoId;
                    document.getElementById('editNombre').value = data.nombre;
                    document.getElementById('editNumeroIdentidad').value = data.numero_identidad;
                    document.getElementById('editDireccion').value = data.direccion_particular;
                    document.getElementById('editCarrera').value = data.carrera;
                    document.getElementById('editAno').value = data.año;
                    document.getElementById('editPais').value = data.pais;
                    document.getElementById('editApartamento').value = data.apartamento;
                    document.getElementById('editEvaJefeResidencia').value = data.evaluacion_jefe_residencia;
                    document.getElementById('editEvaJefeApto').value = data.evaluacion_jefe_apto;
                    document.getElementById('editEvaProfesor').value = data.evaluacion_profesor;
                    editModal.style.display = 'block';
                });
        });
    });

    // Cierra modal al presionar la '×'
    closeEditSpan.onclick = function() {
        editModal.style.display = 'none';
    };

    // Cierra modal al hacer clic fuera de él
    window.addEventListener('click', (event) => {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
    });
});
