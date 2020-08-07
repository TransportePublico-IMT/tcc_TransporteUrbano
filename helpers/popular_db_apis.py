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