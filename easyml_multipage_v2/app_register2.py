from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from dash import Dash

from flask import Flask, render_template, flash, request, url_for, redirect

import sqlite3
import hashlib

from login_app import server

register = Dash(name='register', sharing=True, url_base_pathname='/register/', server=server)

users = sqlite3.connect(os.path.abspath('database/users.db'))
cursor = users.cursor()

register.layout = html.Div([

    html.Img(href='/static/logo2.png', className="logo"),
    
    html.H4('Register'),
    
    html.Div(id='login_div', children=[
        html.H4('Usuário:', style={'border': 'none'}),
        dcc.Input(id='user', min=5, max=15),
    
        html.H4('Senha:', style={'border': 'none'}),
        dcc.Input(id='password', min=5, max=15),
        
        html.Br(),

        dcc.Link('Entrar com conta', href = '/apps/app1', className = 'big button'),

        html.Hr(),
        html.H4('Ou entre como visitante:', style={'border': 'none'}),
        dcc.Link('Entrar sem conta', href = '/apps/app2', className = 'big button')
    ]),    


], className="login_page")




##@app.route('/register/', methods=['POST'])
##def register():
##    username = request.form['username']
##    password = request.form['password']
##
##    try:
##    db_query = cursor.execute("SELECT * FROM users WHERE name='"+username+"';")
##    except:
##
##users.close(   

# Run the server
if __name__ == '__main__':
    server.run(debug=True, port=8050)
