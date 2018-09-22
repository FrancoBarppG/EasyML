
#--------------------------BIBLIOTECAS----------------------------#

#----------Bibliotecas do Dash--------------#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
import dash_table_experiments as dt


#-----------Outras bibliotecas-----------------#
import pandas #pra manipulação de tabelas
from flask import send_from_directory #pra importar arquivos para uso no site
from libs import regs # .py com as funções de simplificação
from libs import plot_functions as plotter #.py com as funções que retornam a figure atualizada do grafico


#---------Bibliotecas Gerais----------------#
import os
import base64
import datetime
import io

#-----------------Database------------------#
import dataset
import sqlite3

from app import app

from app import app
from apps import app1
from apps import app2
from apps import login_app


app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Link(rel = 'stylesheet', href ='/static/style.css'),
    html.Div(id = 'page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    
])

 
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/login':
        return login_app.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug = True)
