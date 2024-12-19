// RENDERIZAR OPCIONES PERSONALIZADAS
function renderEstado(data) {
    return data ? '<span class="badge bg-soft-success text-success">Activo</span>' :
        '<span class="badge bg-soft-danger text-danger">Inactivo</span>';
}

function renderOpciones(row) {
    let accionTexto = row.is_active ? 'Desactivar' : 'Activar';
    return `
        <div class="dropdown">
            <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <b>Acción</b> <i class="mdi mdi-chevron-down"></i>
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#ModalVer" onclick="verUsuario(${row.id})">Información</button>
                <a class="dropdown-item" href="/user/${row.id}/edit">Editar</a>
                <button type="button" class="dropdown-item" onclick="toggleUserStatus(${row.id}, '${row.full_name}', ${row.is_active})">${accionTexto}</button>
                <button type="button" class="dropdown-item" onclick="confirmDeleteUser(${row.id}, '${row.full_name}')">Eliminar</button>
            </div>
        </div>
    `;
}

// MODALES
function toggleUserStatus(userId, fullName, isActive) {
    const modalTitle = isActive ? 'Inactivar Usuario' : 'Activar Usuario';
    const modalBody = `¿Estás seguro de ${isActive ? 'inactivar' : 'activar'} al usuario ${fullName}?`;
    $('#modalToggleTitle').text(modalTitle);
    $('#modalToggleBody').text(modalBody);
    $('#modalToggleConfirm').data('userId', userId).data('isActive', isActive);
    $('#ModalToggle').modal('show');
}

function confirmDeleteUser(userId, fullName) {
    $('#modalEliminarNombre').text(fullName);
    $('#modalConfirmDelete').data('userId', userId);
    $('#ModalEliminar').modal('show');
}

//AJAX
function verUsuario(userId) {
    $.ajax({
        url: url_get_user,
        type: "POST",
        dataType: "json",
        data: { user_id: userId },
        beforeSend: cookie,
        success: function(response) {
            if (response.status === 'success') {
                const user = response.data;
                $('#modalNombre').val(user.full_name);
                $('#modalCorreo').val(user.email);
                $('#modalEstado').html(user.is_active ? '<span class="badge badge-outline-success">Activo</span>' : '<span class="badge badge-outline-danger">Inactivo</span>');

                // Mostrar grupos
                let groupsHTML = '';
                user.groups.forEach(group => {
                    groupsHTML += `<li class="text-reset mb-2 d-block"><i class="mdi mdi-checkbox-blank-circle-outline me-1 text-primary"></i><span class="mb-0 mt-1">${group}</span></li>`;
                });
                $('#modalGroups').html(groupsHTML);

                // Mostrar dashboards
                let dashboardsHTML = '';
                user.direct_dashboards.forEach(dashboard => {
                    dashboardsHTML += `<li class="text-reset mb-2 d-block dashboard-item text-success" data-type="direct"><i class="mdi mdi-checkbox-blank-circle-outline me-1 text-success"></i><span class="mb-0 mt-1">${dashboard[0]}</span></li>`;
                });
                user.group_dashboards.forEach(dashboard => {
                    dashboardsHTML += `<li class="text-reset mb-2 d-block dashboard-item text-warning" data-type="group"><i class="mdi mdi-checkbox-blank-circle-outline me-1 text-warning"></i><span class="mb-0 mt-1">${dashboard[0]}</span></li>`;
                });
                $('#modalDashboards').html(dashboardsHTML);

                // Filtro de búsqueda
                $('#searchDashboards').on('input', function() {
                    let searchText = $(this).val().toLowerCase();
                    $('.dashboard-item').each(function() {
                        const dashboardText = $(this).text().toLowerCase();
                        if (dashboardText.includes(searchText)) {
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
            alert('Error al obtener los detalles del usuario');
        }
    });
}


function confirmToggleUserStatus() {
    var userIdStatus = $('#modalToggleConfirm').data('userId');
    var buttonStatus = $('#modalToggleConfirm');
    $.ajax({
        url: url_toggle_status_user,
        type: "POST",
        dataType: "json",
        data: { user_id: userIdStatus },
        beforeSend: cookie,
        success: function(response) {
            if (response.status === 'success') {
                $('#ModalToggle').modal('hide');
                $('#basic-datatable').DataTable().ajax.reload();
                toastr.success(response.message);
            } else {
                toastr.error(response.message);
            }
        },
        error: function() {
            toastr.error('Error al cambiar el estado del usuario');
        },
        complete: function() {
            buttonStatus.html('Aceptar');
            buttonStatus.prop('disabled', false);
        }
    });
}


function confirmDelete() {
    var userIdDelete = $('#modalConfirmDelete').data('userId');
    var buttonDelete = $('#modalConfirmDelete');
    $.ajax({
        url: url_delete_user,
        type: "POST",
        dataType: "json",
        data: { user_id: userIdDelete },
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
            toastr.error('Error al eliminar el usuario');
        },
        complete: function() {
            buttonDelete.html('Eliminar');
            buttonDelete.prop('disabled', false);
        }

    });
}