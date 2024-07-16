$(document).ready(function() {
    $.extend(true, $.fn.dataTable.defaults, {
        language: {
          sSearch: 'Buscar:',
          paginate: {
            previous: '<i class="mdi mdi-chevron-left"></i>',
            next: '<i class="mdi mdi-chevron-right"></i>'
          },
          "oAria": {
            "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
          },
          "sEmptyTable": "No hay datos disponibles en la tabla",
          "sInfo": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
          "sInfoEmpty": "Mostrando 0 a 0 de 0 entradas",
          "sInfoFiltered": "(filtrado de _MAX_ entradas en total)",
          "sLengthMenu": "Mostrar _MENU_ entradas",
          "sLoadingRecords": "Cargando...",
          "sProcessing": "Procesando...",
          "sZeroRecords": "No se encontraron registros coincidentes",
          "oPaginate": {
            "sFirst": "Primero",
            "sLast": "Último",
            "sNext": "Siguiente",
            "sPrevious": "Anterior"
          }
        }
      });
    });