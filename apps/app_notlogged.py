from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash import Dash

import pandas

import io


max_width_maindiv = '70vw'
min_width_maindiv = '1px'
sidemenu_size = ['25vw', '100vh']
css_sheet = 'style.css'

#--------------------------TODO-----------------------------------------#
   
# Rever a geração de gráficos quando nenhum algoritmo de simplificação foi selecionado


#======================================================================================================================================================

#layout da página:
app_notlogged_layout = html.Div(children = [    

    html.Link(rel = 'stylesheet', href ='/static/style.css'),
    
    html.Div(style = {'width': '320px', 'height': '80px'}, children = [html.Img(src = '/static/logo2.png', style = {'width': '320px', 'height': '80px'})]), 

    html.Div(id='sidemenu',
         style = {'backgroundColor': 'white',
                  'float': 'left',
                  'width': sidemenu_size[0],
                  'height': sidemenu_size[1],
                  'borderRadius': '5px',
                  'borderTop': '2px solid #1975fa',
                  'borderRight': '1px solid #d6d6d6',
                  'borderLeft': '1px solid #d6d6d6',
                  'margin': '0 auto',
                  'padding': '10px'},
         children = [
            html.H4("Tipo do gráfico base"),
            dcc.Dropdown(
                 id = 'type_mainplot',
                 options = [
                     {'label': 'Scatter', 'value': 'scatter'},
                     {'label': 'Bar', 'value': 'bar'}
                    ],
                 value = 'scatter',
                 clearable = False,
                 searchable = False
             ),
            html.H4("Tipo do gráfico 2"),
            dcc.Dropdown(
                 id = 'type_plot2',
                 options = [
                     {'label': 'Scatter', 'value': 'scatter'},
                     {'label': 'Bar', 'value': 'bar'}
                    ],
                 value = 'scatter',
                 clearable = False,
                 searchable = False
             ),

            html.H4("Marcador do gráfico 1"),
            dcc.Dropdown(
                 id = 'type_marker1',
                 options = [
                     {'label': 'Lines', 'value': 'lines'},
                     {'label': 'Bubble', 'value': 'markers'},
                     {'label': 'Fill', 'value': 'fill'}
                    ],
                 value = 'lines',
                 clearable = False,
                 searchable = False
             ),
            
            html.Div( id = 'size_bubble1_div', children = [
                html.H4("Tamanho dos círculos do gráfico 1"),
                dcc.Slider(
                     id = 'size_bubble1',
                     min = 1,
                     max = 15,
                     step = 0.5,
                     value = 5
                 )],
                style = {'display': 'none'}
            ),

            html.H4("Marcador do gráfico 2"),
            dcc.Dropdown(
                 id = 'type_marker2',
                 options = [
                     {'label': 'Lines', 'value': 'lines'},
                     {'label': 'Bubble', 'value': 'markers'},
                     {'label': 'Fill', 'value': 'fill'}
                    ],
                 value = 'lines',
                 clearable = False,
                 searchable = False
             ),    
            html.Div( id = 'size_bubble2_div', children = [
                html.H4("Tamanho dos círculos do gráfico 2"),
                dcc.Slider(
                     id = 'size_bubble2',
                     min = 1,
                     max = 15,
                     step = 0.5,
                     value = 5
                 )],
                style = {'display': 'none'}),
            html.H4("Método de linearização"),
            html.Div( id = 'type_regs_div', children = [
                dcc.Dropdown(
                     id = 'type_regs',
                     options = [
                         {'label': 'MMQ', 'value': 'lsm'},
                         {'label': 'Regressão Linear', 'value': 'linear'},
                         {'label': 'Regressão Logística', 'value': 'logi'},
                         {'label': 'Regressão Logarítmica', 'value': 'log'},
                         {'label': 'Regressão Exponencial', 'value': 'exp'},
                        ],
                     value = 'lsm',
                     clearable = True,
                     searchable = False,
                     placeholder = 'Escolha...'
                 )
                ]),
            html.H4("2D/3D"),
            dcc.Dropdown(
                 id = 'type_dimensions',
                 options = [
                     {'label': '2D', 'value': '2d'},
                     {'label': '3D', 'value': '3d'},
                    ],
                 value = '2d',
                 clearable = False,
                 searchable = False
             ),
            
            html.Button('Refresh', id='reg_button', style = {'backgroundColor': '#1975fa', 'color': 'white', 'width': '100%', 'marginTop': '30px'}),

            ]),
    
    dcc.Tabs(id='tabs', vertical=False, children = [
        
        dcc.Tab(label = 'Graph', id='graph', children = [

            html.Link(rel='stylesheet', href='/static/style.css'),

            html.Div([
                dcc.Upload(
                    id='upload_data',
                    children=html.Div(
                        id='upload_div',
                        children=[
                        'Arraste e solte ou ',
                        html.A('selecione o arquivo')
                    ]),
                    style={
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                )
            ]),
            
            html.Div(children = dt.DataTable(
                rows = [{}],
                columns = ['X', 'Y', 'Z'],
                row_selectable = False,
                filterable = False,
                sortable = False,
                editable = True,
                id = 'datatable',
                max_rows_in_viewport = 5,
                

            ),

            className = 'container'
            ), 

            dcc.Graph(id='output_graph', animate = False, style = {'width': '100%', 'height': '500px', 'display': 'inline-block', 'borderLeft': '1px solid #d6d6d6', 'borderRight': '1px solid #d6d6d6', 'borderBottom': '1px solid #d6d6d6'}),

            

            ]),

            dcc.Tab(label = '', children = [
                html.Link(rel='stylesheet', href='/static/style.css'),
                html.H2("Bem vindo ao EasyML"),
                html.Pre("""
                        Para usar o sistema, aperte em graph acima
                        Se buscar ajuda, clique aqui

                         """),
                html.Img(src = '/static/miotea.png', style = {'width': '50%', 'height': '50%', 'float': 'right', 'margin': '0', 'padding': '0'}),

                dcc.Textarea(id='hidden_text', value='', style={'display': 'none'})

                ],

                disabled = True),
            ],
             
            
             style={        #CSS das tabs
            },
                content_style={
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'borderBottom': '1px solid #d6d6d6',
                'padding': '44px'
            },
                parent_style={
                'maxWidth': max_width_maindiv,
                'margin': '0 auto',
            }
             )
],
                      style = {'position': 'relative'} #CSS da div das tabs
)
    


