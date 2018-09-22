from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from app import app

layout = html.Div([
    
    html.H1('Login'),
    
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


])

