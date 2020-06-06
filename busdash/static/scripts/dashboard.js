function callapi(ajaxUrl, apiBaseUrl, apiUrl, success, paramsDict={}, apiPreUrl='', apiPreUrlMethod='post'){
    $.ajax({
        method: 'POST',
        url: ajaxUrl,
        contentType: "application/json",
        data: JSON.stringify({
            'baseUrl': apiBaseUrl,
            'preUrl': {
                'url': apiPreUrl,
                'method': apiPreUrlMethod
            },
            'url': apiUrl,
            'params': paramsDict
        }),
        success: success
    })
};

$(document).ready(function () {

    //SPTRANS
    function getDataSpTrans (){
        callapi(
            'apis/sptrans',
            'http://api.olhovivo.sptrans.com.br/v2.1',
            '/Posicao/Linha',
            function(data){
                $('#sptrans').text(JSON.stringify(data["json"]));
            },
            {'codigoLinha': '111',},
            '/Login/Autenticar?token=d56f9613a83a7233521ae5413765d15dae0b499967f2a12384ce2f7cd2fe62a9',
        )
    }

    getDataSpTrans();
    setInterval(getDataSpTrans, 5000);
    
    //DIRETODOSTRENS
    situacaoDiretoDosTrens = {};
    function getDataDiretoDosTrens (){
        situacaoDiretoDosTrens = {};
        var today = new Date();
        situacaoDiretoDosTrens['atualizacao'] = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        callapi(
            'apis/direto-dos-trens',
            'https://www.diretodostrens.com.br/api',
            '/status',
            function(data){
                $('#chartDiretoDosTrens').html("" + (data["plot"]));
            }
        )
    }

    getDataDiretoDosTrens();
    //atualiza a cada 20 segundos
    setInterval(getDataDiretoDosTrens, 20000);
    
})