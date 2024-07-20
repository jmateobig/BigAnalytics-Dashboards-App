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
function verDashboard(dashboardId) {
    $.ajax({
        url: url_get_dashboard, // Asegúrate de definir esta URL en tu JavaScript
        type: "POST",
        dataType: "json",
        data: { dashboard_id: dashboardId },
        beforeSend: cookie,
        success: function(response) {
            if (response.status === 'success') {
                const dashboard = response.data;
                $('#modalNombre').text(dashboard.name);
                let usuariosHTML = '';
                dashboard.users.forEach(user => {
                    usuariosHTML += `
                        <div class="inbox-item">
                            <p class="inbox-item-author">
                                ${user.is_active ? '<i class="mdi mdi-checkbox-blank-circle-outline me-1 text-success"></i>' : '<i class="mdi mdi-checkbox-blank-circle-outline me-1 text-danger"></i>'}
                                ${user.username}
                            </p>
                            <p class="inbox-item-text">${user.full_name}</p>
                        </div>
                    `;
                });
                $('#modalUsuarios').html(usuariosHTML);
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