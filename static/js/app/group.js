// RENDERIZAR OPCIONES PERSONALIZADAS
function renderOpciones(row) {
    return `
        <div class="dropdown">
            <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <b>Acción</b> <i class="mdi mdi-chevron-down"></i>
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#ModalVer" onclick="verGrupo(${row.id})">Información</button>
                <a class="dropdown-item" href="/group/${row.id}/edit/">Editar</a>
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
                $('#modalNombre').val(group.name);
                $('#modalCategoria').val(group.category);
                let usuariosHTML = '';
                group.users.forEach(user => {
                    const userClass = user.is_active === true ? 'text-success' : 'text-danger';
                    usuariosHTML += `<li class="text-reset mb-2 d-block usuario-item ${userClass}"><i class="mdi mdi-checkbox-blank-circle-outline me-1 ${userClass}"></i><span class="mb-0 mt-1">${user.full_name} (${user.email})</span></li>`;
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
                toastr.success(response.message);
            } else {
                toastr.error(response.message);
            }
        },
        error: function () {
            toastr.error('Error al eliminar el grupo');
        },
        complete: function() {
            buttonDelete.html('Eliminar');
            buttonDelete.prop('disabled', false);
        }
    });
}