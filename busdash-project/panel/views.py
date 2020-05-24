from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from . import plots
import urllib
import requests
import json

def home(request):
    return render(request, 'panel/home.html', {'page_title':'SA-Trans Dashboard'})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

def sptrans_login(request):
    token = request.GET['token']
    response = requests.post(f'http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}')
    return JsonResponse({'success':response.json()})

def api_get_data(request):
    response = ''
    data = json.loads(request.body)
    pre_url = data['preUrl']
    base_url = data['baseUrl']
    url = data['url']
    params = '?'
    for param in data['params']:
        params += (param + '=' + data['params'][param])

    call = base_url + url + params

    if pre_url['url'] != '':
        if pre_url['method'].lower() == 'get':
            pre_response = requests.get(base_url + pre_url['url'])
            response = requests.get(call, cookies=pre_response.cookies)
        elif pre_url['method'].lower() == 'post':
            pre_response = requests.post(base_url + pre_url['url'])
            response = requests.get(call, cookies=pre_response.cookies)
    else:
        response = requests.get(call)

    json_returned = response.json()
    return json_returned

@csrf_exempt
def direto_dos_trens(request):
    #Chamada da API para pegar dados e criar um dicionario já filtrado
    data = api_get_data(request)
    situacaoDiretoDosTrens = {}
    for linha in data:
        if linha['situacao'] == "Operação Encerrada" or linha['situacao'] == "Operações Encerradas":
            linha['situacao'] = "Operação Encerrada"
        if linha['situacao'] in situacaoDiretoDosTrens:
            if 'descricao' in linha:
                situacaoDiretoDosTrens[linha['situacao']].append({'linha': linha['codigo'], 'descricao': linha['descricao']})
            else:
                situacaoDiretoDosTrens[linha['situacao']].append({'linha': linha['codigo']})
        else:
            situacaoDiretoDosTrens[linha['situacao']] = []
            if 'descricao' in linha:
                situacaoDiretoDosTrens[linha['situacao']].append({'linha': linha['codigo'], 'descricao': linha['descricao']})
            else:
                situacaoDiretoDosTrens[linha['situacao']].append({'linha': linha['codigo']})
    #Criação das listas com base no dicionario para popular o gráfico
    label_list = ["Situação"]
    parent_list = [""]
    hovertext_list = [""]
    color_list = ["fff"]
    for situacao in situacaoDiretoDosTrens:
        label_list.append(situacao)
        parent_list.append("Situação")
        hovertext_list.append("")
        #cores
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
            #cores
            if situacao == "Operação Normal":
                color_list.append("#28a745")
            elif situacao == "Operação Parcial":
                color_list.append("#ffc107")
            elif situacao == "Paralisada":
                color_list.append("#dc3545")
            else:
                color_list.append("#ffc107")
            if 'descricao' in linha:
                counter = 0
                descricao = ""
                #Isso serve para quebrar as linhas da descrição colocando <br>, senão ficava gigante no hover
                for letra in linha["descricao"]:
                    descricao += letra
                    counter += 1
                    if counter % 50 == 0:
                        descricao += "<br>"
                hovertext_list.append(descricao)
            else:
                hovertext_list.append("")

    plot_div = plots.direto_dos_trens(label_list, parent_list, hovertext_list, color_list)    

    return JsonResponse({"json": situacaoDiretoDosTrens, "plot": plot_div})

@csrf_exempt
def sptrans(request):
    data = api_get_data(request)
    return JsonResponse({"json": data, "plot": {}})
    # return HttpResponse(status=200)