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

app = dash.Dash()
server = app.server
app.scripts.config.serve_locally=True
app.css.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True


app.css.append_css({"external_url": os.path.abspath('/static/style.css')})


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.abspath('/static')
    return send_from_directory(static_folder, path)        

