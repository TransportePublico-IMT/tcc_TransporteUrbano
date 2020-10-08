import datetime
import json
import urllib

import requests


def api_get_data(
    apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl="", apiPreUrlMethod="post"
):
    response = ""
    base_url = apiBaseUrl
    url = apiUrl
    params = "?"
    for param in paramsDict:
        params += param + "=" + paramsDict[param] + "&"
    params += "/"
    if params == "?/":
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


def direto_dos_trens(
    apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl="", apiPreUrlMethod="post"
):
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
            if linha["descricao"] is not None:
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

    ret = {
        "label_list": label_list,
        "parent_list": parent_list,
        "hovertext_list": hovertext_list,
        "color_list": color_list,
    }
    return ret


def sp_trans_localizacao(
    apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl="", apiPreUrlMethod="post"
):
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)
    lon_list = []
    lat_list = []
    hover_text_list = []
    for linha in data["l"]:
        for bus in linha["vs"]:
            lat_list.append(bus["py"])
            lon_list.append(bus["px"])
            hover_text_list.append(
                f"PREFIXO: {str(bus['p'])}<br>LETREIRO: {str(linha['c'])}<br>CÓDIGO LINHA: {str(linha['cl'])}"
            )

    ret = {
        "lon_list": lon_list,
        "lat_list": lat_list,
        "hover_text_list": hover_text_list,
    }
    return ret


def sp_trans_velocidade(
    apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl="", apiPreUrlMethod="post"
):
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)
    lista_onibus_velocidade = []
    for onibus_velocidade in data:
        lista_lat = []
        lista_lon = []
        for coordenada in onibus_velocidade["coordenadas"]:
            if coordenada["latitude"] is None or coordenada["longitude"] is None:
                lista_lat.append("")
                lista_lon.append("")
            else:
                lista_lat.append(coordenada["latitude"])
                lista_lon.append(coordenada["longitude"])
        lista_lat.append("")
        lista_lon.append("")
        obj = {
            "nome": onibus_velocidade["nome"],
            "vel_trecho": onibus_velocidade["vel_trecho"],
            "vel_via": onibus_velocidade["vel_via"],
            "trecho": onibus_velocidade["trecho"],
            "extensao": onibus_velocidade["extensao"],
            "tempo": onibus_velocidade["tempo"],
            "latitudes": lista_lat,
            "longitudes": lista_lon,
        }
        lista_onibus_velocidade.append(obj)
    return lista_onibus_velocidade


def paradas(apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl="", apiPreUrlMethod="post"):
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)
    lon_list = []
    lat_list = []
    hover_text_list = []
    for parada in data:
        lat_list.append(parada["latitude"])
        lon_list.append(parada["longitude"])
        hover_text_list.append(parada["nome"])

    ret = {
        "lon_list": lon_list,
        "lat_list": lat_list,
        "hover_text_list": hover_text_list,
    }
    return ret


def onibus_historico():
    dias_list = []
    quantidade_list = []
    weekday_name = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

    primeiro = True
    for i in range(8):
        dia = datetime.datetime.today() - datetime.timedelta(days=i)
        dia_mes = dia.strftime("%d/%m")
        dia_semana = dia.weekday()
        if primeiro:
            primeiro = False
            dias_list.append(f"Hoje<br>({dia_mes})")
        else:
            dias_list.append(f"{weekday_name[dia_semana]}<br>({dia_mes})")

        data_inicial = datetime.datetime.combine(dia, datetime.datetime.min.time())
        data_final = datetime.datetime.combine(dia, datetime.datetime.max.time())
        #somar mais 3 horas para utc
        data_inicial += datetime.timedelta(hours=3)
        data_final += datetime.timedelta(hours=3)

        data = api_get_data(
            "http://localhost/api",
            "/onibus-posicao/quantidade/",
            paramsDict={
                "data-inicial": data_inicial.strftime("%Y-%m-%d %H:%M:%S"),
                "data-final": data_final.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
        quantidade_list.append(data["quantidade"])

    dias_list.reverse()
    quantidade_list.reverse()

    ret = {"dias_list": dias_list, "quantidade_list": quantidade_list}
    return ret


def climatempo_tempo(
    apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl="", apiPreUrlMethod="post"
):
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)
    ret = data
    return ret


def cards_lotacao(
    apiBaseUrl, apiUrl, paramsDict={}, apiPreUrl="", apiPreUrlMethod="post"
):
    data = api_get_data(apiBaseUrl, apiUrl, paramsDict, apiPreUrl, apiPreUrlMethod)
    ret = data
    return ret
