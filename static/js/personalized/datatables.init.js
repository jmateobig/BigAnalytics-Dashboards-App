// Configuración de DataTable
var spanishLanguageConfig = {
    "sLengthMenu": "Mostrar _MENU_ registros",
    "sZeroRecords": "No se encontraron resultados",
    "sEmptyTable": "Ningún dato disponible en esta tabla",
    "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
    "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
    "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
    "sInfoPostFix": "",
    "sSearch": "Buscar:",
    "sUrl": "",
    "sInfoThousands": ",",
    "sLoadingRecords": "Cargando...",
    "oPaginate": {
        "sFirst": "Primero",
        "sLast": "Último",
        "sNext": "Siguiente",
        "sPrevious": "Anterior"
    },
    "oAria": {
        "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
        "sSortDescending": ": Activar para ordenar la columna de manera descendente"
    }
};



function getSettingsDatatable () {
    return {
        scrollCollapse: true,
        lengthChange: true,
        language: spanishLanguageConfig,
        processing: true,
        serverSide: true,
        ordering: true,
        searchDelay: 1500
    }
}

function loadTableData() {
    const settings_datatable = getSettingsDatatable();
    $('#data-table').DataTable({
        ...settings_datatable,
        columns: columns,
        ajax: {
            url: url,
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            dataSrc: 'data',
            beforeSend: beforeSend,
            data: function (d) {
                return JSON.stringify({
                    draw: d.draw,
                    start: d.start,
                    length: d.length,
                    search: d.search.value,
                    orderColumn: d.order[0].column,
                    orderDir: d.order[0].dir,
                    page: d.start / d.length + 1
                });
            }
        }
    });
}


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