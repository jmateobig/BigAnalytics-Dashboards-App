// RENDERIZAR OPCIONES PERSONALIZADAS
function renderOpciones(row) {
    return `
        <div class="dropdown">
            <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <b>Acción</b> <i class="mdi mdi-chevron-down"></i>
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#ModalVer" onclick="verDashboard(${row.id})">Ver</button>
                <a class="dropdown-item" href="/dashboard/edit/${row.id}/">Editar</a>
                <button type="button" class="dropdown-item" onclick="confirmDeleteDashboard(${row.id}, '${row.name}')">Eliminar</button>
            </div>
        </div>
    `;
}

// MODALES
function confirmDeleteDashboard(dashboardId, dashboardName) {
    $('#modalEliminarNombre').text(dashboardName);
    $('#modalConfirmDelete').data('dashboardId', dashboardId);
    $('#ModalEliminar').modal('show');
}

//AJAX
// Función para mostrar detalles del dashboard en el modal
function verDashboard(dashboardId) {
    $.ajax({
        url: url_get_dashboard,
        type: "POST",
        dataType: "json",
        data: { dashboard_id: dashboardId },
        beforeSend: cookie,
        success: function(response) {
            if (response.status === 'success') {
                const dashboard = response.data;
                $('#modalNombre').val(dashboard.name);
                $('#modalTitulo').val(dashboard.title);
                $('#modalDescripcion').val(dashboard.description);
                $('#modalUrl').val(dashboard.url);

                // Grupos
                let gruposHTML = '';
                dashboard.groups.forEach(group => {
                    gruposHTML += `<li class="text-reset mb-2 d-block"><i class="mdi mdi-checkbox-blank-circle-outline me-1 text-primary"></i><span class="mb-0 mt-1">${group}</span></li>`;
                });
                $('#modalGrupos').html(gruposHTML);

                // Usuarios
                let usuariosHTML = '';
                dashboard.users.forEach(user => {
                    const userClass = user.flag === 'success' ? 'text-success' : 'text-warning';
                    usuariosHTML += `<li class="text-reset mb-2 d-block usuario-item ${userClass}"><i class="mdi mdi-checkbox-blank-circle-outline me-1 ${userClass}"></i><span class="mb-0 mt-1">${user.full_name}</span></li>`;
                });
                $('#modalUsuarios').html(usuariosHTML);

                // Agregar event listener para la búsqueda
                $('#searchUsuarios').on('input', function() {
                    const searchText = $(this).val().toLowerCase();
                    $('#modalUsuarios .usuario-item').each(function() {
                        const userText = $(this).text().toLowerCase();
                        if (userText.includes(searchText)) {
                            $(this).removeClass('hide-item').addClass('show-item');
                        } else {
                            $(this).removeClass('show-item').addClass('hide-item');
                        }
                    });
                });

            } else {
                alert(response.message);
            }
        },
        error: function() {
            alert('Error al obtener los detalles del dashboard');
        }
    });
}




function confirmDelete() {
    var dashboardIdDelete = $('#modalConfirmDelete').data('dashboardId');
    var buttonDelete = $('#modalConfirmDelete');
    $.ajax({
        url: url_delete_dashboard,
        type: "POST",
        dataType: "json",
        data: { dashboard_id: dashboardIdDelete },
        beforeSend: cookie,
        success: function (response) {
            if (response.status === 'success') {
                $('#ModalEliminar').modal('hide');
                $('#basic-datatable').DataTable().ajax.reload();
                toastr.success(response.message);
            } else {
                toastr.error(response.message);
            }
        },
        error: function () {
            toastr.error('Error al eliminar el dashboard');
        },
        complete: function() {
            buttonDelete.html('Eliminar');
            buttonDelete.prop('disabled', false);
        }
    });
}