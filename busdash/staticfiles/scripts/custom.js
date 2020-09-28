$(document).ready(function() {
    $('iframe').each(function(){  
    $(this).attr('scrolling','no');
    });

    var table = $("#table-onibus-lotacao").DataTable({
        //"ajax": {url:"/api/onibus-lotacao/ultimos/?intervalo=1", dataSrc:""},
        "ajax": {url:"/api/onibus-lotacao/ultimos/", dataSrc:""},
        "columns": [
            {"data": "id_onibus"},
            {"data": "id_linha"},
            {"data": "lotacao"},
            {"data": "latitude"},
            {"data": "longitude"},
            {"data": "data_inclusao"}
        ],
        columnDefs: [{//2020-08-22T16:10:56.404988Z
            targets: 5,
            render: $.fn.dataTable.render.moment('YYYY-MM-DDTHH:mm:ss.SSSSSSZ', 'DD/MM/YYYY - HH:mm:ss')
        }],
        "scrollY": "160px",
        "oLanguage": {
            "sEmptyTable": "Nenhum registro encontrado",
            "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
            "sInfoFiltered": "(Filtrados de _MAX_ registros)",
            "sInfoPostFix": "",
            "sInfoThousands": ".",
            "sLengthMenu": "_MENU_ resultados por página",
            "sLoadingRecords": "Carregando...",
            "sProcessing": "Processando...",
            "sZeroRecords": "Nenhum registro encontrado",
            "sSearch": "Pesquisar",
            "oPaginate": {
                "sNext": "Próximo",
                "sPrevious": "Anterior",
                "sFirst": "Primeiro",
                "sLast": "Último"
            },
            "oAria": {
                "sSortAscending": ": Ordenar colunas de forma ascendente",
                "sSortDescending": ": Ordenar colunas de forma descendente"
            },
            "select": {
                "rows": {
                    "_": "Selecionado %d linhas",
                    "0": "Nenhuma linha selecionada",
                    "1": "Selecionado 1 linha"
                }
            },
            "buttons": {
                "copy": "Copiar para a área de transferência",
                "copyTitle": "Cópia bem sucedida",
                "copySuccess": {
                    "1": "Uma linha copiada com sucesso",
                    "_": "%d linhas copiadas com sucesso"
                }
            }
        }
  });
  setInterval(function(){
      table.ajax.reload(null, false);
  },5000);

})