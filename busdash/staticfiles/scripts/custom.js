$(document).ready(function() {
    $('iframe').each(function(){  
    $(this).attr('scrolling','no');
    });

    var portugues = {
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
        columnDefs: [
            { width: 70, targets: 0 },
            { width: 60, targets: 1 },
            { width: 70, targets: 2 },
            { width: 60, targets: 3, render: $.fn.dataTable.render.number(',', '.', 4) },
            { width: 60, targets: 4, render: $.fn.dataTable.render.number(',', '.', 4)},
            {
            targets: 5,
            width: 100,
            render: $.fn.dataTable.render.moment('YYYY-MM-DDTHH:mm:ss.SSSSSSZ', 'DD/MM/YYYY - HH:mm:ss')
        }],
        "scrollY": "160px",
        "scrollX": true,
        "oLanguage": portugues
    });

    var tableEventos = $("#table-eventos").DataTable({
        //"ajax": {url:"/api/onibus-lotacao/ultimos/?intervalo=1", dataSrc:""},
        "ajax": {url:"/api/eventos/", dataSrc:""},
        "columns": [
            {"data": "nome"},
            {"data": "endereco"},
            {"data": "data_info"},
            {"data": "link",
                "render": function(data, type, row, meta){
                    if(type === 'display'){
                        data = '<a href="' + data + '">' + data + '</a>';
                    }
        
                    return data;
                }
            }
        ],
        columnDefs: [
            { width: 70, targets: 0 },
            { width: 90, targets: 1 },
            { width: 70, targets: 2 },
            { width: 70, targets: 3 }
        ],
        fixedColumns: true,
        "scrollY": "300px",
        "scrollX": true,
        "oLanguage": portugues
    });

    setInterval(function(){
        tableEventos.ajax.reload(null, false);
    },5000);

    setInterval(function(){
        table.ajax.reload(null, false);
    },5000);

})