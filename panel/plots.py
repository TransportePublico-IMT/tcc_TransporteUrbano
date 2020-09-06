import datetime
import os
from os.path import dirname, join

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from django.shortcuts import render
from django_plotly_dash import DjangoDash
from dotenv import load_dotenv
from plotly.offline import plot

from . import apis

pio.renderers.default = "svg"

# Create .env file path.
dotenv_path = join(dirname(__file__), "../.ENV")

# Load file from the path.
load_dotenv(dotenv_path)


plot_direto_dos_trens = DjangoDash("DiretoDosTrens")
plot_direto_dos_trens.layout = html.Div(
    [
        dcc.Graph(id="situacao-trens-metros"),
        dcc.Interval(id="direto-dos-trens-update", interval=5000, n_intervals=0),
    ]
)

plot_localizacao_sptrans = DjangoDash("LocSptrans")
plot_localizacao_sptrans.layout = html.Div(
    [
        dcc.Graph(id="loc-sptrans"),
        dcc.Interval(id="loc-sptrans-update", interval=5000, n_intervals=0),
    ]
)

plot_cards_lotacao = DjangoDash("CardsLotacao", add_bootstrap_links=True)
plot_cards_lotacao.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Ônibus vazios",
                                style={"font-size": "18px"},
                                className="py-1 text-center",
                            ),
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "n/a",
                                        id="qtd-vazio",
                                        className="card-title text-center py-0 mb-1",
                                        style={"font-size": "42px"},
                                    ),
                                    html.P(
                                        "Atualizado: n/a",
                                        id="atualizacao-vazio",
                                        className="card-text text-center",
                                    ),
                                ],
                                className="py-2",
                            ),
                        ],
                        color="success",
                        inverse=True,
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Ônibus normais",
                                style={"font-size": "18px"},
                                className="py-1 text-center",
                            ),
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "n/a",
                                        id="qtd-normal",
                                        className="card-title text-center py-0 mb-1",
                                        style={"font-size": "42px"},
                                    ),
                                    html.P(
                                        "Atualizado: n/a",
                                        id="atualizacao-normal",
                                        className="card-text text-center",
                                    ),
                                ],
                                className="py-2",
                            ),
                        ],
                        color="primary",
                        inverse=True,
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Ônibus cheios",
                                style={"font-size": "18px"},
                                className="py-1 text-center",
                            ),
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "n/a",
                                        id="qtd-cheio",
                                        className="card-title text-center py-0 mb-1",
                                        style={"font-size": "42px"},
                                    ),
                                    html.P(
                                        "Atualizado: n/a",
                                        id="atualizacao-cheio",
                                        className="card-text text-center",
                                    ),
                                ],
                                className="py-2",
                            ),
                        ],
                        color="danger",
                        inverse=True,
                    )
                ),
            ],
            className="mb-4",
        ),
        dcc.Interval(
            id="cards-lotacao-update", interval=10000, n_intervals=0  # in milliseconds
        ),
    ]
)

plot_tempo_climatempo = DjangoDash("ClimaTemp", add_bootstrap_links=True)
plot_tempo_climatempo.layout = html.Div(
    [
        daq.Thermometer(
            id="tempo_climaTemp",
            min=0,
            max=45,
            value=0,
            height=175,
            color="#c0c0c0",
            showCurrentValue=True,
            units="°C",
        ),
        dcc.Interval(id="temp-climatempo-update", interval=9000000, n_intervals=0),
    ]
)


@plot_direto_dos_trens.callback(
    dash.dependencies.Output("situacao-trens-metros", "figure"),
    [dash.dependencies.Input("direto-dos-trens-update", "n_intervals")],
)
def update_direto_dos_trens(self):
    plot_info = apis.direto_dos_trens(
        "https://www.diretodostrens.com.br/api", "/status"
    )
    data = go.Sunburst(
        labels=plot_info["label_list"],
        parents=plot_info["parent_list"],
        hovertext=plot_info["hovertext_list"],
        hovertemplate="<b>%{label}</b> <br>%{hovertext}<extra></extra>",
        textfont={
            "size": 15,
            "family": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"',
        },
        marker={"colors": plot_info["color_list"]},
    )
    ret = {
        "data": [data],
        "layout": go.Layout(
            margin=dict(t=0, b=0, l=0, r=0), height=250, uirevision=True
        ),
    }
    return ret


@plot_localizacao_sptrans.callback(
    dash.dependencies.Output("loc-sptrans", "figure"),
    [dash.dependencies.Input("loc-sptrans-update", "n_intervals")],
)
def sp_trans_localizacao(data):
    mapbox_access_token = os.getenv("MAPBOXAPI")
    plot_info = apis.sp_trans_localizacao(
        "http://api.olhovivo.sptrans.com.br/v2.1",
        "/Posicao",
        apiPreUrl="/Login/Autenticar?token=" + os.getenv("OLHOVIVO"),
    )
    data = go.Scattermapbox(
        lat=plot_info["lat_list"],
        lon=plot_info["lon_list"],
        mode="markers",
        marker=go.scattermapbox.Marker(symbol=plot_info["symbol_list"], size=12),
    )

    ret = {
        "data": [data],
        "layout": go.Layout(
            hovermode="closest",
            hoverdistance=1,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(lat=-23.55, lon=-46.64),
                pitch=0,
                zoom=9,
                style="light",
            ),
            uirevision=True,
            margin=dict(t=0, b=0, l=0, r=0),
            height=250,
        ),
    }
    return ret


@plot_tempo_climatempo.callback(
    [
        dash.dependencies.Output("tempo_climaTemp", "value"),
        dash.dependencies.Output("tempo_climaTemp", "color"),
    ],
    [dash.dependencies.Input("temp-climatempo-update", "n_intervals")],
)
def update_climatempo(self):
    idCity_STAndre = 3667
    token = os.getenv("CLIMATEMPO")
    url = "http://apiadvisor.climatempo.com.br/api/v1/weather/locale/"
    urlplus = str(idCity_STAndre) + "/current?token=" + token
    plot_info = apis.climatempo_tempo(url, urlplus)
    temp = plot_info["data"]["temperature"]
    color = ""
    if temp <= 15:
        color = "#007BFF"
    elif temp > 15 and temp < 25:
        color = "#ffc107"
    else:
        color = "#DC3545"
    return temp, color


@plot_cards_lotacao.callback(
    [
        dash.dependencies.Output("qtd-vazio", "children"),
        dash.dependencies.Output("qtd-normal", "children"),
        dash.dependencies.Output("qtd-cheio", "children"),
        dash.dependencies.Output("atualizacao-vazio", "children"),
        dash.dependencies.Output("atualizacao-normal", "children"),
        dash.dependencies.Output("atualizacao-cheio", "children"),
    ],
    [dash.dependencies.Input("cards-lotacao-update", "n_intervals")],
)
def update_cards_lotacao(self):
    vazio = apis.cards_lotacao(
        "http://localhost:8000/api", "/onibus-lotacao", {"lotacao": "vazio"}
    )
    normal = apis.cards_lotacao(
        "http://localhost:8000/api", "/onibus-lotacao", {"lotacao": "normal"}
    )
    cheio = apis.cards_lotacao(
        "http://localhost:8000/api", "/onibus-lotacao", {"lotacao": "cheio"}
    )
    now = datetime.datetime.now()
    horario = "Atualizado: " + now.strftime("%H:%M:%S")
    return [
        html.Span(len(vazio)),
        html.Span(len(normal)),
        html.Span(len(cheio)),
        html.Span(horario),
        html.Span(horario),
        html.Span(horario),
    ]
