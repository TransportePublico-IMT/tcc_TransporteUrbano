import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from django_plotly_dash import DjangoDash

import plotly.io as pio
pio.renderers.default = "svg"

import plotly.graph_objects as go
from django.shortcuts import render
from plotly.offline import plot
from . import apis

plot_direto_dos_trens = DjangoDash('DiretoDosTrens')
plot_direto_dos_trens.layout = html.Div([
    dcc.Graph(id='situacao-trens-metros'),
    dcc.Interval(
        id='direto-dos-trens-update',
        interval=5000,
        n_intervals=0
    )
])

plot_localizacao_sptrans = DjangoDash('LocSptrans')
plot_localizacao_sptrans.layout = html.Div([
    dcc.Graph(id='loc-sptrans'),
    dcc.Interval(
        id='loc-sptrans-update',
        interval=5000,
        n_intervals=0
    )
])


@plot_direto_dos_trens.callback(
    dash.dependencies.Output('situacao-trens-metros', 'figure'),
    [dash.dependencies.Input('direto-dos-trens-update', 'n_intervals')])
def update_direto_dos_trens(self):
    plot_info = apis.direto_dos_trens(
        'https://www.diretodostrens.com.br/api',
        '/status'
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

@plot_localizacao_sptrans.callback(
    dash.dependencies.Output('loc-sptrans', 'figure'),
    [dash.dependencies.Input('loc-sptrans-update', 'n_intervals')])
def sp_trans_localizacao(data):
    mapbox_access_token = "pk.eyJ1IjoibHVjYWV6ZWxsbmVyIiwiYSI6ImNrYjRiNm12ZDBodHkyc284M3FteHRyNGgifQ.73HUnz3EYhNZsilwkR4OdQ"
    plot_info = apis.sp_trans_localizacao(
        'http://api.olhovivo.sptrans.com.br/v2.1',
        '/Posicao',
        apiPreUrl='/Login/Autenticar?token=d56f9613a83a7233521ae5413765d15dae0b499967f2a12384ce2f7cd2fe62a9'
    )
    data = go.Scattermapbox(
        lat=plot_info['lat_list'],
        lon=plot_info['lon_list'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            symbol=plot_info['symbol_list'],
            size=12
        )
    )
    
    ret = {'data': [data],
            'layout': go.Layout(hovermode='closest',
                                hoverdistance=1,
                                
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
                                margin=dict(t=0, b=0, l=0, r=0),height=250)}
    return ret