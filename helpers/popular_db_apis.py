import json
import urllib
from panel.apis import api_get_data
from trem.models import Trem
import requests


def popular_trens_metros():
    data = api_get_data(
        'https://www.diretodostrens.com.br/api',
        '/status'
    )
    
    list_trens = []
    for i in data:
        descricao = None
        if 'descricao' in i:
            descricao = i['descricao']
        trem = {
            'id_linha': i["codigo"],
            'data_ocorrencia': i["criado"],
            'descricao': descricao,
            'ultima_atualizacao': i["modificado"],
            'situacao': i["situacao"]
        }
        list_trens.append(trem)
    
    url = "http://localhost:8000/api/trens/"
    headers = {
        'Content-Type': 'application/json',
        'Connection' : 'keep-alive',
        'Accept': "*/*"
    }
    data = {'t': list_trens}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    return r.json()

def popular_climatempo():
    idCity_STAndre = 3667
    token = "cd640a1a7fd7767e9afc268efcb06882"
    url = "http://apiadvisor.climatempo.com.br/api/v1/weather/locale/" + str(idCity_STAndre) + "/current?token=" + token
    data = api_get_data(url)
    list_clima = []
    i = data["data"]
    clima = {
        'id_cidade': data["id"],
        'temperatura': i['temperature'],
        'direcao_vento': i["wind_direction"],
        'velocidade_vento': i["wind_velocity"],
        'umidade': i["humidity"],
        'condicao': i["condition"],
        'pressao': i["pressure"],
        #'icone': i["icon"], #????? vamos colocar?
        'sensacao': i["sensation"],
        'date': i["date"]
    }
    list_clima.append(clima)
    url = "http://localhost:8000/api/climatempo/"
    headers = {
        'Content-Type': 'application/json',
        'Connection' : 'keep-alive',
        'Accept': "*/*"
    }
    data = {'ct': list_clima}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    return r.json()