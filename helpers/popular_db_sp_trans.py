import json
import time
import urllib

import requests

from linha.models import Linha
from panel.apis import api_get_data
from parada.models import Parada

from dotenv import load_dotenv
import os
from os.path import join, dirname

# Create .env file path.
dotenv_path = join(dirname(__file__), '../.ENV')
# Load file from the path.
load_dotenv(dotenv_path)

def popular_paradas():
    data = api_get_data(
        "http://api.olhovivo.sptrans.com.br/v2.1",
        "/Parada/Buscar",
        paramsDict={"termosBusca": ""},
        apiPreUrl="/Login/Autenticar?token="+os.getenv('OLHOVIVO'),
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
        apiPreUrl="/Login/Autenticar?token="+os.getenv('OLHOVIVO'),
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
        apiPreUrl="/Login/Autenticar?token="+os.getenv('OLHOVIVO'),
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
