# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.express as px
# import plotly.graph_objects as go

# from django_plotly_dash import DjangoDash

# import plotly.io as pio
# pio.renderers.default = "svg"
  
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go

def direto_dos_trens(label_list, parent_list, hovertext_list, color_list):
    trace = go.Sunburst(
        labels=label_list,
        parents=parent_list,
        hovertext=hovertext_list,
        hovertemplate='<b>%{label}</b> <br>%{hovertext}<extra></extra>',
        textfont={"size": 15, "family": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"'},
        marker={"colors": color_list},
        
    )
    fig = go.Figure(data=[trace], layout=go.Layout(margin=dict(t=0,b=0,l=0,r=0), height=300))
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div