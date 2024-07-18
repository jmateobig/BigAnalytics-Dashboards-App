// RENDERIZAR OPCIONES PERSONALIZADAS
function renderEstado(data) {
    return data ? '<span class="badge bg-soft-success text-success">Activo</span>' :
        '<span class="badge bg-soft-danger text-danger">Inactivo</span>';
}

function renderOpciones(row) {
    let accionTexto = row.is_active ? 'Inactivar' : 'Activar';
    return `
        <div class="dropdown">
            <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <b>Acción</b> <i class="mdi mdi-chevron-down"></i>
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#ModalVer" onclick="verUsuario(${row.id})">Ver</button>
                <a class="dropdown-item" href="/user/edit/${row.id}/">Editar</a>
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
                let gruposHTML = '';
                user.groups.forEach(group => {
                    gruposHTML += `<a href="javascript: void(0);" class="text-reset mb-2 d-block"><i class="mdi mdi-checkbox-blank-circle-outline me-1 text-success"></i><span class="mb-0 mt-1">${group}</span></a>`;
                });
                $('#modalGrupos').html(gruposHTML);
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
            } else {
                alert(response.message);
            }
        },
        error: function() {
            alert('Error al cambiar el estado del usuario');
        }
    });
}


function confirmDelete() {
    var userIdDelete = $('#modalConfirmDelete').data('userId');
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
            } else {
                alert(response.message);
            }
        },
        error: function () {
            alert('Error al eliminar el usuario');
        }
    });
}