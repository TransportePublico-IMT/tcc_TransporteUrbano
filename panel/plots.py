import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from django_plotly_dash import DjangoDash
import datetime
from dotenv import load_dotenv
import pandas as pd
import os
from os.path import join, dirname
import plotly.io as pio
pio.renderers.default = "svg"
import plotly.graph_objects as go
from django.shortcuts import render
from plotly.offline import plot
from . import apis
from itertools import chain

# Create .env file path.
dotenv_path = join(dirname(__file__), '../.ENV')
# Load file from the path.
load_dotenv(dotenv_path)

plot_direto_dos_trens = DjangoDash('DiretoDosTrens')
plot_direto_dos_trens.layout = html.Div([
    dcc.Graph(id='situacao-trens-metros'),
    dcc.Interval(
        id='direto-dos-trens-update',
        interval=5000,
        n_intervals=0
    )
])

plot_onibus_historico = DjangoDash('HistoricoOnibus', add_bootstrap_links=True)
plot_onibus_historico.layout = html.Div([
    html.Span(
        "QUANTIDADE DE ÔNIBUS QUE CIRCULARAM - ÚLTIMOS 7 DIAS",
        style={"font-size": "18px", "font-weight":"500", "display": "block", "text-align": "center", "color": "#6c757d"}
    ),
    dcc.Graph(id='historico-onibus'),
    dcc.Interval(
        id='historico-onibus-update',
        interval=20000,
        n_intervals=0
    )
])

plot_localizacao_sptrans = DjangoDash('LocSptrans')
plot_localizacao_sptrans.layout = html.Div([
    dcc.Graph(id='loc-sptrans'),
    dcc.Interval(
        id='loc-sptrans-update',
        interval=60000,
        n_intervals=0
    )
])

plot_cards_lotacao = DjangoDash('CardsLotacao', add_bootstrap_links=True)
plot_cards_lotacao.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(dbc.Card(
                [dbc.CardHeader("Ônibus vazios", style={"font-size": "18px"}, className="py-1 text-center"),
                dbc.CardBody(
                    [
                        html.H5("n/a", id="qtd-vazio", className="card-title text-center py-0 mb-1", style={"font-size": "42px"}),
                        html.P("Atualizado: n/a", id="atualizacao-vazio", className="card-text text-center"),
                    ],
                className="py-2")],
                color="success", inverse=True)),
            dbc.Col(dbc.Card(
                [dbc.CardHeader("Ônibus normais", style={"font-size": "18px"}, className="py-1 text-center"),
                dbc.CardBody(
                    [
                        html.H5("n/a", id="qtd-normal", className="card-title text-center py-0 mb-1", style={"font-size": "42px"}),
                        html.P("Atualizado: n/a", id="atualizacao-normal", className="card-text text-center"),
                    ],
                className="py-2")],
                color="primary", inverse=True)),
            dbc.Col(dbc.Card(
                [dbc.CardHeader("Ônibus cheios", style={"font-size": "18px"}, className="py-1 text-center"),
                dbc.CardBody(
                    [
                        html.H5("n/a", id="qtd-cheio", className="card-title text-center py-0 mb-1", style={"font-size": "42px"}),
                        html.P("Atualizado: n/a", id="atualizacao-cheio", className="card-text text-center"),
                    ],
                className="py-2")],
                color="danger", inverse=True)),
        ],
        className="mb-4"
    ),
    dcc.Interval(
        id='cards-lotacao-update',
        interval=10000, # in milliseconds
        n_intervals=0
    )
])

plot_tempo_climatempo = DjangoDash('ClimaTemp', add_bootstrap_links=True)
plot_tempo_climatempo.layout = html.Div([
    daq.Thermometer(
        id='tempo_climaTemp',
        min=0,
        max=45,
        value=0,
        height=140,
        color="#c0c0c0",
        showCurrentValue=True,
        units=""
    ),
    html.Div([
        html.Span(
            "CARREGANDO...",
            id='condicao_tempo',
            style={"font-size": "18px", "font-weight":"500", "display": "block", "text-align": "center", "color": "#6c757d"}
        )
    ]),
    dcc.Interval(
        id='temp-climatempo-update',
        interval=9000000,
        n_intervals=0
    )
])

plot_onibus_agora = DjangoDash('OnibusAgora', add_bootstrap_links=True)
plot_onibus_agora.layout = html.Div([
    html.H3(
        "Tempo Real",
        style={"font-size": "18px", "font-weight":"500", "display": "block", "text-align": "center", "color": "#6c757d", "text-transform": "uppercase"}
    ),
    dbc.Card(
        [dbc.CardHeader("Ônibus Ativos", style={"font-size": "18px"}, className="py-1 text-center"),
        dbc.CardBody(
            [
                html.H5("n/a", id="qtd-onibus-agora", className="card-title text-center py-0 mb-1", style={"font-size": "42px"}),
            ],
        className="py-2")],
        color="success", className="mb-2", inverse=True
    ),
    dbc.Card(
        [dbc.CardHeader("Linhas Ativas", style={"font-size": "18px"}, className="py-1 text-center"),
        dbc.CardBody(
            [
                html.H5("n/a", id="qtd-linhas-agora", className="card-title text-center py-0 mb-1", style={"font-size": "42px"}),
            ],
        className="py-2")],
        color="success", inverse=True
    ),
    dcc.Interval(
        id='onibus-agora-update',
        interval=5000,
        n_intervals=0
    )
])

@plot_direto_dos_trens.callback(
    dash.dependencies.Output('situacao-trens-metros', 'figure'),
    [dash.dependencies.Input('direto-dos-trens-update', 'n_intervals')])
def update_direto_dos_trens(self):
    plot_info = apis.direto_dos_trens(
        'http://localhost:8000/api',
        '/trens/ultimos'
    )
    data = go.Sunburst(
        labels=plot_info['label_list'],
        parents=plot_info['parent_list'],
        hovertext=plot_info['hovertext_list'],
        hovertemplate="<b>%{label}</b> <br>%{hovertext}<extra></extra>",
        textfont={
            "size": 15,
            "family": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
        },
        marker={"colors": plot_info['color_list']},
        )
    ret = {'data': [data],
           'layout': go.Layout(margin=dict(t=0, b=0, l=0, r=0), height=250,uirevision= True)}
    return ret

@plot_onibus_historico.callback(
    dash.dependencies.Output('historico-onibus', 'figure'),
    [dash.dependencies.Input('historico-onibus-update', 'n_intervals')])
def update_onibus_historico(self):
    data = apis.onibus_historico()
    plot_info = {
                'Dia':  data['dias_list'],
                'Quantidade': data['quantidade_list']
                }

    data = go.Bar(  x=plot_info['Dia'],
                    y=plot_info['Quantidade'],
                    text=plot_info['Quantidade'],
                    textposition='auto',
                    marker_color='#007BFF'
    )
    ret = {'data': [data],
           'layout': go.Layout(margin=dict(t=10, b=30, l=30, r=0), height=220, hovermode='closest', uirevision= True)}
    return ret

@plot_localizacao_sptrans.callback(
    dash.dependencies.Output('loc-sptrans', 'figure'),
    [dash.dependencies.Input('loc-sptrans-update', 'n_intervals')])
def sp_trans_localizacao(data):
    lista_traces = []
    mapbox_access_token = os.getenv('MAPBOXAPI')
    plot_info_onibus = apis.sp_trans_localizacao(
        'http://api.olhovivo.sptrans.com.br/v2.1',
        '/Posicao',
        apiPreUrl='/Login/Autenticar?token='+os.getenv('OLHOVIVO')
    )
    plot_info_paradas = apis.paradas(
        'http://localhost:8000',
        '/api/paradas/'
    )
    onibus = go.Scattermapbox(
        lat=plot_info_onibus['lat_list'],
        lon=plot_info_onibus['lon_list'],
        hovertext= plot_info_onibus['hover_text_list'],
        mode='markers+text',
        hoverinfo='text',
        name='Ônibus',
        marker=go.scattermapbox.Marker(
            size=10,
            color='#212529',
            opacity=1
        )
    )    
    lista_traces.append(onibus)

    paradas = go.Scattermapbox(
        lat=plot_info_paradas['lat_list'],
        lon=plot_info_paradas['lon_list'],
        hovertext= plot_info_paradas['hover_text_list'],
        mode='markers+text',
        hoverinfo='text',
        textposition='bottom center',
        text=plot_info_paradas['hover_text_list'],
        name='Parada',
        marker=go.scattermapbox.Marker(
            size=14,
            color='#007bff',
            opacity=1
        )
    )    
    lista_traces.append(paradas)
 
    traces = {
        'verde': {'lat': [], 'lon': [], 'nome': [], 'vel_trecho': [], 'vel_via': [], 'extensao': [], 'tempo': [], 'trecho': [], 'color': '#28a745', 'name': 'Rápido'},
        'amarelo': {'lat': [], 'lon': [], 'nome': [], 'vel_trecho': [], 'vel_via': [], 'extensao': [], 'tempo': [], 'trecho': [], 'color': '#ffc107', 'name': 'Intenso'},
        'vermelho': {'lat': [], 'lon': [], 'nome': [], 'vel_trecho': [], 'vel_via': [], 'extensao': [], 'tempo': [], 'trecho': [], 'color': '#dc3545', 'name': 'Lento'}
    }
    velocidades = apis.sp_trans_velocidade('http://localhost:8000','/api/onibus-velocidade/ultimos/')
    for velocidade in velocidades:
        color = ''

        if velocidade['vel_trecho'] != None and velocidade['vel_via'] != None:
            lat = velocidade['latitudes']
            lon = velocidade['longitudes']
            nome=velocidade['nome']
            vel_trecho=velocidade['vel_trecho']
            vel_via=velocidade['vel_via']
            extensao=velocidade['extensao']
            tempo=velocidade['tempo']
            trecho=velocidade['trecho']
            if velocidade['vel_trecho'] >= 23:
                traces['verde']['lat'].append(lat)
                traces['verde']['lon'].append(lon)
                traces['verde']['nome'].append(nome)
                traces['verde']['trecho'].append(trecho)
                traces['verde']['vel_trecho'].append(vel_trecho)
                traces['verde']['vel_via'].append(vel_via)
                traces['verde']['extensao'].append(extensao)
                traces['verde']['tempo'].append(tempo)
            elif velocidade['vel_trecho'] >= 20:
                traces['amarelo']['lat'].append(lat)
                traces['amarelo']['lon'].append(lon)
                traces['amarelo']['trecho'].append(trecho)
                traces['amarelo']['nome'].append(nome)
                traces['amarelo']['vel_trecho'].append(vel_trecho)
                traces['amarelo']['vel_via'].append(vel_via)
                traces['amarelo']['extensao'].append(extensao)
                traces['amarelo']['tempo'].append(tempo)
            else:
                traces['vermelho']['lat'].append(lat)
                traces['vermelho']['lon'].append(lon)
                traces['vermelho']['nome'].append(nome)
                traces['vermelho']['trecho'].append(trecho)
                traces['vermelho']['vel_via'].append(vel_via)
                traces['vermelho']['vel_trecho'].append(vel_trecho)
                traces['vermelho']['extensao'].append(extensao)
                traces['vermelho']['tempo'].append(tempo)
    
    
    
    for trace in traces:
        lista_hover_text = []
        k=0
        for i in traces[trace]['lat']:
            for j in i:
                lista_hover_text.append(
                    f'''Via: {traces[trace]['nome'][k]}
                    <br>Velocidade da via: {traces[trace]['vel_via'][k]} km/h
                    <br>Trecho: {traces[trace]['trecho'][k]}
                    <br>Velocidade do trecho: {traces[trace]['vel_trecho'][k]} km/h
                    <br>Extensão: {traces[trace]['extensao'][k]} m
                    <br>Tempo: {traces[trace]['tempo'][k]}'''
                    )
            k+=1

        data = go.Scattermapbox(
            mode = "lines",
            lat = list(chain.from_iterable(traces[trace]['lat'])),
            lon = list(chain.from_iterable(traces[trace]['lon'])),
            hoverinfo='text',
            hovertext = lista_hover_text,
            name = traces[trace]['name'],
            line={'color': traces[trace]['color']},
        )
        lista_traces.append(data)
 
    ret = {'data': lista_traces,
            'layout': go.Layout(hovermode='closest',
                                hoverdistance=1,
                                legend=dict(
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01
                                    ),
                                mapbox=dict(
                                    accesstoken=mapbox_access_token,
                                    bearing=0,
                                    center=go.layout.mapbox.Center(
                                        lat=-23.55,
                                        lon=-46.64
                                    ),
                                    pitch=0,
                                    zoom=9,
                                    style='light',
                                ),
                                uirevision= True,
                                margin=dict(t=0, b=0, l=0, r=0),height=440)}
    return ret

@plot_onibus_agora.callback(
    [dash.dependencies.Output('qtd-onibus-agora', 'children'),
    dash.dependencies.Output('qtd-linhas-agora', 'children')],
    [dash.dependencies.Input('onibus-agora-update', 'n_intervals')])
def update_onibus_agora(data):
    info_agora = apis.api_get_data(
        'http://api.olhovivo.sptrans.com.br/v2.1',
        '/Posicao',
        apiPreUrl='/Login/Autenticar?token='+os.getenv('OLHOVIVO')
    )

    qtd_linhas = len(info_agora['l'])
    qtd_onibus = 0
    for linha in info_agora['l']:
        qtd_onibus += linha['qv']

    return [html.Span(qtd_onibus), html.Span(qtd_linhas)]

@plot_tempo_climatempo.callback(
    [dash.dependencies.Output('tempo_climaTemp', 'value'),
    dash.dependencies.Output('tempo_climaTemp', 'color'),
    dash.dependencies.Output('condicao_tempo', 'children')],
    [dash.dependencies.Input('temp-climatempo-update', 'n_intervals')])
def update_climatempo(self):
    url = "http://localhost:8000/api"
    urlplus = "/climatempo/ultimo/"
    plot_info = apis.climatempo_tempo(url,urlplus)
    temp = float(plot_info["temperatura"])
    color=""
    condicao = plot_info["condicao"].upper()
    if temp <= 15:
        color = "#007BFF"
    elif temp > 15 and temp < 25:
        color = "#ffc107"
    else:
        color = "#DC3545"
    return temp, color, condicao

@plot_cards_lotacao.callback(
            [dash.dependencies.Output('qtd-vazio', 'children'),
            dash.dependencies.Output('qtd-normal', 'children'),
            dash.dependencies.Output('qtd-cheio', 'children'),
            dash.dependencies.Output('atualizacao-vazio', 'children'),
            dash.dependencies.Output('atualizacao-normal', 'children'),
            dash.dependencies.Output('atualizacao-cheio', 'children'),],
            [dash.dependencies.Input('cards-lotacao-update', 'n_intervals')])
def update_cards_lotacao(self):
    vazio = apis.cards_lotacao(
        'http://localhost:8000/api',
        '/onibus-lotacao/ultimos/',
        {
            "lotacao":"vazio",
            #"intervalo": "1",
        }
    )
    normal = apis.cards_lotacao(
        'http://localhost:8000/api',
        '/onibus-lotacao/ultimos/',
        {
            "lotacao":"normal",
            #"intervalo": "1",
        }
    )
    cheio = apis.cards_lotacao(
        'http://localhost:8000/api',
        '/onibus-lotacao/ultimos/',
        {
            "lotacao":"cheio",
            #"intervalo": "1",
        }
    )
    now = datetime.datetime.now()
    horario = "Atualizado: " + now.strftime("%H:%M:%S")
    return [
        html.Span(len(vazio)), html.Span(len(normal)), html.Span(len(cheio)), html.Span(horario), html.Span(horario), html.Span(horario)
    ]
