// RENDERIZAR OPCIONES PERSONALIZADAS
function renderOpciones(row) {
    return `
        <div class="dropdown">
            <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <b>Acción</b> <i class="mdi mdi-chevron-down"></i>
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#ModalVer" onclick="verGrupo(${row.id})">Ver</button>
                <a class="dropdown-item" href="/group/edit/${row.id}/">Editar</a>
                <button type="button" class="dropdown-item" onclick="confirmDeleteGroup(${row.id}, '${row.name}')">Eliminar</button>
            </div>
        </div>
    `;
}

// MODALES
function confirmDeleteGroup(groupId, groupName) {
    $('#modalEliminarNombre').text(groupName);
    $('#modalConfirmDelete').data('groupId', groupId);
    $('#ModalEliminar').modal('show');
}

//AJAX
function verGrupo(groupId) {
    $.ajax({
        url: url_get_group, // Asegúrate de definir esta URL en tu JavaScript
        type: "POST",
        dataType: "json",
        data: { group_id: groupId },
        beforeSend: cookie,
        success: function(response) {
            if (response.status === 'success') {
                const group = response.data;
                $('#modalNombre').text(group.name);
                let usuariosHTML = '';
                group.users.forEach(user => {
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
            alert('Error al obtener los detalles del grupo');
        }
    });
}


function confirmDelete() {
    var groupIdDelete = $('#modalConfirmDelete').data('groupId');
    var buttonDelete = $('#modalConfirmDelete');
    $.ajax({
        url: url_delete_group,
        type: "POST",
        dataType: "json",
        data: { group_id: groupIdDelete },
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
            alert('Error al eliminar el grupo');
        },
        complete: function() {
            buttonDelete.html('Eliminar');
            buttonDelete.prop('disabled', false);
        }
    });
}