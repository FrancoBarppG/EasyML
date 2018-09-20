
#--------------------------BIBLIOTECAS----------------------------#

#----------Bibliotecas do Dash--------------#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dt


#-----------Outras bibliotecas-----------------#
import pandas #pra manipulação de tabelas
from flask import send_from_directory #pra importar arquivos para uso no site
import regs # .py com as funções de simplificação
import plot_functions as plotter #.py com as funções que retornam a figure atualizada do grafico


#---------Bibliotecas Gerais----------------#
import os
import base64
import datetime
import io


#------BASE-------#
app = dash.Dash()
server = app.server
#-----------------#

#--------------------------PARÂMETROS GERAIS----------------------------#

max_width_maindiv = '70vw'
min_width_maindiv = '1px'
sidemenu_size = ['25vw', '100vh']
css_sheet = 'style.css'

app.scripts.config.serve_locally=True
app.css.config.serve_locally = True
#app.config['suppress_callback_exceptions'] = True

#Página base:
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>EasyML</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
    </body>
</html>
'''

#--------------------------TODO-----------------------------------------#
   
# Rever a geração de gráficos quando nenhum algoritmo de simplificação foi selecionado


#======================================================================================================================================================




#incorpora o /static/ no projeto
@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


#inclui a sheet de css no projeto
app.css.append_css({"external_url": "/static/{}".format(css_sheet)})


#função pra dar parse no conteúdo do arquivo de upload
def parse_upload_contents(contents, filename):
    content_type, content_string = contents[0].split(',')
    filename = filename[0]
    decoded = base64.b64decode(content_string)
    try:

        if '.csv' in filename:
            table_data = pandas.read_csv(
                io.StringIO(decoded.decode('utf-8')))

        elif '.xls' in filename:
            table_data = pandas.read_excel(io.BytesIO(decoded))
            
    except Exception as e:
        print(e)
        return None # TODO: colocar alert aqui

    return table_data


#layout da página:
app.layout = html.Div(children = [    

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
    
    
    
# Coloca o arquivo de upload na planilha
@app.callback(Output('datatable', 'rows'),
              [Input('upload_data', 'contents'),
               Input('upload_data', 'filename')])

def update_output(contents, filename):
    if contents is not None:
        df = parse_upload_contents(contents, filename)
        if df is not None:
            return df.to_dict('records')
        else:
            return [{}]
    else:
        return [{}]


#Muda o dropdown de algoritmos de simplificação de acordo com as dimesões (2d ou 3d)
@app.callback(
    Output(component_id='type_regs_div', component_property='children'),
    [Input(component_id='type_dimensions', component_property='value')])

def update_children(value):
    if value == '2d':
        return dcc.Dropdown(
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
    elif value == '3d':
        return dcc.Dropdown(
             id = 'type_regs',
             options = [
                 {'label': 'MMQ 3d', 'value': 'lsm3d'},
                 {'label': 'Regressão Linear 3d', 'value': 'linear3d'},
                 {'label': 'Regressão Logística 3d', 'value': 'logi3d'},
                 {'label': 'Regressão Logarítmica 3d', 'value': 'log3d'},
                 {'label': 'Regressão Exponencial 3d', 'value': 'exp3d'},
                ],
             value = 'lsm3d',
             clearable = True,
             searchable = False,
             placeholder = 'Escolha...'
         )


#Se for usado marcador, coloca o slider de tamanho do marcador
@app.callback(
    Output(component_id='size_bubble1_div', component_property='style'),
    [Input(component_id='type_marker1', component_property='value')])

def update_size_bubble1(mode1):
    if mode1 == 'markers':
        return None
    elif mode1 == 'lines' or mode1 == 'fill':
        return {'display': 'none'}

@app.callback(
    Output(component_id='size_bubble2_div', component_property='style'),
    [Input(component_id='type_marker2', component_property='value')])

def update_size_bubble2(mode2):
    if mode2 == 'markers':
        return None
    elif mode2 == 'lines' or mode2 == 'fill':
        return {'display': 'none'}



#Se for colocado em 2d, vai automaticamente pra 'lines', se for 3d, vai automaticamente pra 'bubbles'
@app.callback(
    Output(component_id='type_marker1', component_property='value'),
    [Input(component_id='type_dimensions', component_property='value')])

def to_bubble_1(dimensions):
    if dimensions == '3d':
        return 'bubbles'
    else:
        return 'lines'

@app.callback(
    Output(component_id='type_marker2', component_property='value'),
    [Input(component_id='type_dimensions', component_property='value')])

def to_bubble_2(dimensions):
    if dimensions == '3d':
        return 'bubbles'
    else:
        return 'lines'


               
# Atualiza o gráfico de acordo com a planilha e os outros parâmetros
@app.callback(
    Output(component_id='output_graph', component_property='figure'),
    [Input(component_id='reg_button', component_property='n_clicks'),
     Input(component_id='datatable', component_property='rows'),
     Input(component_id='type_mainplot', component_property='value'),
     Input(component_id='type_plot2', component_property='value'),
     Input(component_id='type_regs', component_property='value'),
     Input(component_id='type_marker1', component_property='value'),
     Input(component_id='type_marker2', component_property='value'),
     Input(component_id='type_dimensions', component_property='value'),
     Input(component_id='size_bubble1', component_property='value'),
     Input(component_id='size_bubble2', component_property='value')])

def update_figure(n_clicks, rows, value, value2, reg_type, mode1, mode2, dimensions, size1, size2):

##    print('\n---------DEBUG--------------')
##    print(n_clicks, repr(n_clicks))
##    print(rows, repr(rows))
##    print(value, repr(value))
##    print(value2, repr(n_clicks))
##    print(reg_type, repr(reg_type))
    
    if n_clicks is not None and len(rows[0]) is not 0:

        # Se tiver clickado uma vez, vai fazer a reg e atualizar o grafico
        

        dff = pandas.DataFrame(rows)

        x = dff['X']
        y = dff['Y']
        z = dff['Z']

##        print('\n---------DEBUG 2--------------')
##        print(repr(x))
##        print(repr(y))
##        print(repr(z))

        #Se for 2d, usa o algoritmo de simplificação escolhido e gera o gráfico
        if dimensions == '2d':
            x_2, y_2 = regs.choose_reg_2d(reg_type, x, y)
            return plotter.generate_plot2d_2(x, y, value, 'Dados', 'Gráfico 2d', x_2, y_2, value2, 'Hipótese', mode1, mode2, size1, size2)
        #Se for 3d, usa o algoritmo de simplificação escolhido e gera o gráfico
        elif dimensions == '3d':
            z = ['0' if z[i] == None else z[i] for i in range(len(z))]
            x_2, y_2, z_2 = regs.choose_reg_3d(reg_type, x, y, z)
            ##################################################################TODO#################################################### colocar o 3d_2
            return plotter.generate_plot3d_2(x, y, z, value+'3d', None, {'size': size1, 'opacity': '0.7'}, 'nome3d', 'Gráfico 3d', x_2, y_2, z_2, value+'3d', None, {'size': size2, 'opacity': '0.7'}, 'nome3d2')

    #Caso não tenha sido escolhido algoritmo de simplificação gera o gráfico 2d ou 3d
    elif len(rows[0]) is not 0:
        
        dff = pandas.DataFrame(rows)
        
        x = dff['X']
        y = dff['Y']
        z = dff['Z']

        #REVER
        
        print(len(z))

        if dimensions == '2d':
            return plotter.generate_plot2d(x, y, value, 'Dados', 'Gráfico 2d')
        elif dimensions == '3d':
            z = ['0' if z[i] == None else z[i] for i in range(len(z))]
            return plotter.generate_plot3d(x, y, z, value+'3d', None, {'size': size1, 'opacity': '0.7'}, 'nome3d', 'Gráfico 3d')


if __name__ == '__main__':
    app.run_server(debug=True)
