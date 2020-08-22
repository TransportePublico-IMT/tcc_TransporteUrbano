import json
import urllib

import requests

def api_get_data(apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl='', apiPreUrlMethod='post'):
    response = ""
    base_url = apiBaseUrl
    url = apiUrl
    params = "?"
    for param in paramsDict:
        params += param + "=" + paramsDict[param]
    if params == "?":
        params = ""

    call = base_url + url + params
    if apiPreUrl != "":
        if apiPreUrlMethod.lower() == "get":
            pre_response = requests.get(base_url + apiPreUrl)
            response = requests.get(call, cookies=pre_response.cookies)
        elif apiPreUrlMethod.lower() == "post":
            pre_response = requests.post(base_url + apiPreUrl)
            response = requests.get(call, cookies=pre_response.cookies)
    else:
        response = requests.get(call)

    json_returned = response.json()
    return json_returned

def direto_dos_trens(apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl='', apiPreUrlMethod='post'):
    # Chamada da API para pegar dados e criar um dicionario já filtrado
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)
    situacaoDiretoDosTrens = {}
    for linha in data:
        if (
            linha["situacao"] == "Operação Encerrada"
            or linha["situacao"] == "Operações Encerradas"
        ):
            linha["situacao"] = "Operação Encerrada"
        if linha["situacao"] in situacaoDiretoDosTrens:
            if "descricao" in linha:
                situacaoDiretoDosTrens[linha["situacao"]].append(
                    {"linha": linha["id_linha"], "descricao": linha["descricao"]}
                )
            else:
                situacaoDiretoDosTrens[linha["situacao"]].append(
                    {"linha": linha["id_linha"]}
                )
        else:
            situacaoDiretoDosTrens[linha["situacao"]] = []
            if "descricao" in linha:
                situacaoDiretoDosTrens[linha["situacao"]].append(
                    {"linha": linha["id_linha"], "descricao": linha["descricao"]}
                )
            else:
                situacaoDiretoDosTrens[linha["situacao"]].append(
                    {"linha": linha["id_linha"]}
                )
    # Criação das listas com base no dicionario para popular o gráfico
    label_list = ["Situação"]
    parent_list = [""]
    hovertext_list = [""]
    color_list = ["fff"]
    for situacao in situacaoDiretoDosTrens:
        label_list.append(situacao)
        parent_list.append("Situação")
        hovertext_list.append("")
        # cores
        if situacao == "Operação Normal":
            color_list.append("#28a745")
        elif situacao == "Operação Parcial":
            color_list.append("#ffc107")
        elif situacao == "Paralisada":
            color_list.append("#dc3545")
        else:
            color_list.append("#ffc107")
        for linha in situacaoDiretoDosTrens[situacao]:
            label_list.append(linha["linha"])
            parent_list.append(situacao)
            # cores
            if situacao == "Operação Normal":
                color_list.append("#28a745")
            elif situacao == "Operação Parcial":
                color_list.append("#ffc107")
            elif situacao == "Paralisada":
                color_list.append("#dc3545")
            else:
                color_list.append("#ffc107")
            if linha["descricao"] != None:
                counter = 0
                descricao = ""
                # Isso serve para quebrar as linhas da descrição colocando <br>, senão ficava gigante no hover
                for letra in linha["descricao"]:
                    descricao += letra
                    counter += 1
                    if counter % 50 == 0:
                        descricao += "<br>"
                hovertext_list.append(descricao)
            else:
                hovertext_list.append("")

    ret = {'label_list': label_list, 'parent_list': parent_list, 'hovertext_list': hovertext_list, 'color_list': color_list}
    return ret

def sp_trans_localizacao(apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl='', apiPreUrlMethod='post'):
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)
    lon_list = []
    lat_list = []
    symbol_list = []
    for linha in data["l"]:
        for bus in linha["vs"]:
            lat_list.append(bus["py"])
            lon_list.append(bus["px"])
            symbol_list.append("bus")
    
    ret = {'lon_list': lon_list, 'lat_list': lat_list, 'symbol_list': symbol_list}
    return ret

def climatempo_tempo(apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl='', apiPreUrlMethod='post'):
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)    
    ret = data
    return ret

def cards_lotacao(apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl='', apiPreUrlMethod='post'):
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)
    ret = data
    return ret