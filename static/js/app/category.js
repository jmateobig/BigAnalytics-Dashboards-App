// RENDERIZAR OPCIONES PERSONALIZADAS
function renderOpciones(row) {
    return `
        <div class="dropdown">
            <button class="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <b>Acción</b> <i class="mdi mdi-chevron-down"></i>
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#ModalVer" onclick="verCategoria(${row.id})">Información</button>
                <a class="dropdown-item" href="/category/${row.id}/edit">Editar</a>
                <button type="button" class="dropdown-item" onclick="confirmDeleteCategory(${row.id}, '${row.name}')">Eliminar</button>
            </div>
        </div>
    `;
}

// MODALES
function confirmDeleteCategory(categoryId, categoryName) {
    $('#modalEliminarNombre').text(categoryName);
    $('#modalConfirmDelete').data('categoryId', categoryId);
    $('#ModalEliminar').modal('show');
}

//AJAX
// Función para mostrar detalles de la categoria en el modal
function verCategoria(categoryId) {
    $.ajax({
        url: url_get_category,
        type: "POST",
        dataType: "json",
        data: { category_id: categoryId },
        beforeSend: cookie,
        success: function(response) {
            if (response.status === 'success') {
                const category = response.data;
                $('#modalNombre').val(category.name);
                $('#modalDescripcion').val(category.description);

                // Grupos
                let groupsHTML = '';
                category.groups.forEach(group => {
                    groupsHTML += `<li class="text-reset mb-2 d-block grupo-item"><i class="mdi mdi-checkbox-blank-circle-outline me-1 text-primary"></i><span class="mb-0 mt-1">${group}</span></li>`;
                });
                $('#modalGrupos').html(groupsHTML);

                // Agregar event listener para la búsqueda
                $('#searchGrupos').on('input', function() {
                    const searchText = $(this).val().toLowerCase();
                    $('#modalGrupos .grupo-item').each(function() {
                        const grupoText = $(this).text().toLowerCase();
                        if (grupoText.includes(searchText)) {
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
            alert('Error al obtener los detalles de la categoria');
        }
    });
}


function confirmDelete() {
    var categoryIdDelete = $('#modalConfirmDelete').data('categoryId');
    var buttonDelete = $('#modalConfirmDelete');
    $.ajax({
        url: url_delete_category,
        type: "POST",
        dataType: "json",
        data: { category_id: categoryIdDelete },
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
            toastr.error('Error al eliminar la Categoria');
        },
        complete: function() {
            buttonDelete.html('Eliminar');
            buttonDelete.prop('disabled', false);
        }
    });
}