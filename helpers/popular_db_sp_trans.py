import json
import time
import urllib

import requests

from linha.models import Linha
from panel.apis import api_get_data
from parada.models import Parada


def popular_paradas():
    data = api_get_data(
        "http://api.olhovivo.sptrans.com.br/v2.1",
        "/Parada/Buscar",
        paramsDict={"termosBusca": ""},
        apiPreUrl="/Login/Autenticar?token=d56f9613a83a7233521ae5413765d15dae0b499967f2a12384ce2f7cd2fe62a9",
    )

    list_paradas = []
    for i in data:
        parada = {
            "id_parada": i["cp"],
            "nome": i["np"],
            "endereco": i["ed"],
            "latitude": i["py"],
            "longitude": i["px"],
        }
        list_paradas.append(parada)

    url = "http://localhost/api/paradas/"
    headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Accept": "*/*",
    }
    data = {"p": list_paradas}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    return r.json()


def popular_linhas():
    data = api_get_data(
        "http://api.olhovivo.sptrans.com.br/v2.1",
        "/Posicao",
        apiPreUrl="/Login/Autenticar?token=d56f9613a83a7233521ae5413765d15dae0b499967f2a12384ce2f7cd2fe62a9",
    )
    list_linhas = []
    for i in data["l"]:
        linha = {
            "id_linha": i["cl"],
            "letreiro": i["c"],
            "sentido": i["sl"],
            "letreiro_destino": i["lt0"],
            "letreiro_origem": i["lt1"],
        }
        list_linhas.append(linha)

    url = "http://localhost/api/linhas/"
    headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Accept": "*/*",
    }
    data = {"l": list_linhas}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    return r.json()


def popular_onibus():
    data = api_get_data(
        "http://api.olhovivo.sptrans.com.br/v2.1",
        "/Posicao",
        apiPreUrl="/Login/Autenticar?token=d56f9613a83a7233521ae5413765d15dae0b499967f2a12384ce2f7cd2fe62a9",
    )
    list_onibus = []
    for i in data["l"]:
        for y in i["vs"]:
            onibus = {
                "id_onibus": y["p"],
                "onibus_deficiente": y["a"],
                "horario_atualizacao_localizacao": y["ta"],
                "latitude": y["py"],
                "longitude": y["px"],
                "id_linha": i["cl"],
                "frota": i["qv"],
            }
            list_onibus.append(onibus)

    url = "http://localhost/api/onibus-posicao/"
    headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Accept": "*/*",
    }
    data = {"o": list_onibus}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    return r.json()
