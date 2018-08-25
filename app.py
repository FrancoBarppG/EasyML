import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dt

import pandas
from flask import send_from_directory

import os
import base64
import datetime
import io

import regs # .py com as funções de simplificação
import plot_functions as plotter

app = dash.Dash()
server = app.server

N_TABLES = 100

app.scripts.config.serve_locally=True
app.css.config.serve_locally = True
#app.config['suppress_callback_exceptions'] = True

#--------------------------PARÂMETROS----------------------------#

max_width_maindiv = '70vw'
min_width_maindiv = '1px'
sidemenu_size = ['25vw', '100vh']





#----------------------------------------------------------------#




@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


app.css.append_css({"external_url": "/static/{}".format('style.css')})
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})




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




app.layout = html.Div(children = [


    html.Link(rel='stylesheet', href='/static/style.css'),
    
    html.Div(id='header_img', style = {'width': '320px', 'height': '80px'}),

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
                     {'label': 'Line', 'value': 'line'},
                     {'label': 'Bar', 'value': 'bar'},
                     {'label': 'Bubble', 'value': 'bubble'},
                    ],
                 value = 'scatter',
                 clearable = False
             ),
            html.H4("Tipo do gráfico 2"),
            dcc.Dropdown(
                 id = 'type_plot2',
                 options = [
                     {'label': 'Scatter', 'value': 'scatter'},
                     {'label': 'Line', 'value': 'line'},
                     {'label': 'Bar', 'value': 'bar'}
                    ],
                 value = 'scatter',
                 clearable = False
             ),

            html.H4("Marcador do gráfico 1"),
            dcc.Dropdown(
                 id = 'type_marker1',
                 options = [
                     {'label': 'Lines', 'value': 'lines'},
                     {'label': 'Bubble', 'value': 'markers'},
                    ],
                 value = 'lines',
                 clearable = False
             ),
            html.H4("Marcador do gráfico 2"),
            dcc.Dropdown(
                 id = 'type_marker2',
                 options = [
                     {'label': 'Lines', 'value': 'lines'},
                     {'label': 'Bubble', 'value': 'markers'},
                    ],
                 value = 'lines',
                 clearable = False
             ),
            
            html.H4("Método de linearização"),
            dcc.Dropdown(
                 id = 'type_regs',
                 options = [
                     {'label': 'MMQ', 'value': 'lsm'},
                     {'label': 'Regressão Linear', 'value': 'linear'},
                     {'label': 'Regressão Logística', 'value': 'log'}
                    ],
                 value = 'lsm',
                 clearable = True
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

            dcc.Graph(id='output_graph', style = {'width': '100%', 'height': '100%', 'display': 'inline-block', 'borderLeft': '1px solid #d6d6d6', 'borderRight': '1px solid #d6d6d6', 'borderBottom': '1px solid #d6d6d6'}),

            

            ]),

            dcc.Tab(label = '', children = [
                html.Link(rel='stylesheet', href='/static/style.css'),
                html.H2("Bem vindo ao EasyML"),
                html.Pre("""Para usar o sistema, aperte em graph acima
                        Se buscar ajuda, clique aqui

                         """),
                ],

                disabled = True),
            ],
             
        
                
             style={
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
]
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


                      
# Atualiza o gráfico se a planilha for editada
@app.callback(
    Output(component_id='output_graph', component_property='figure'),
    [Input(component_id='reg_button', component_property='n_clicks'),
     Input(component_id='datatable', component_property='rows'),
     Input(component_id='type_mainplot', component_property='value'),
     Input(component_id='type_plot2', component_property='value'),
     Input(component_id='type_regs', component_property='value'),
     Input(component_id='type_marker1', component_property='value'),
     Input(component_id='type_marker2', component_property='value')])

def update_figure(n_clicks, rows, value, value2, reg_type, mode1, mode2):

    print('\n---------DEBUG--------------')
    print(n_clicks, repr(n_clicks))
    print(rows, repr(rows))
    print(value, repr(value))
    print(value2, repr(n_clicks))
    print(reg_type, repr(reg_type))
    
    if n_clicks is not None and len(rows[0]) is not 0:

        # Se tiver clickado uma vez, vai fazer a reg e atualizar o grafico
        

        dff = pandas.DataFrame(rows)

        x = dff['X']
        y = dff['Y']
        z = dff['Z']

        print('\n---------DEBUG 2--------------')
        print(repr(x))
        print(repr(y))
        print(repr(z))

        

        if len(z)==0 or all(z[i] == None for i in range(len(z))):
            x_2, y_2 = regs.choose_reg(reg_type, x, y)
            return plotter.generate_plot2d_2(x, y, value, 'nome2d', 'titulo2d', x_2, y_2, value2, 'nome2d2', mode1, mode2)

        else:
            return plotter.generate_plot3d(x, y, z, value+'3d', None, {'size': '10', 'opacity': '0.7'}, 'nome3d', 'titulo3d') ################################### colocar filtro dos tipos de 3d e 2d


    elif len(rows[0]) is not 0:
        
        dff = pandas.DataFrame(rows)
        
        x = dff['X']
        y = dff['Y']
        z = dff['Z']


        """
        for i in range(N_TABLES):
            z_index = rows[i]['Z']
            if z_index=='':
                z_index = '0'
            z_indices.extend(z_index)"""
        #REVER
        
        print(len(z))

        if len(z)==0 or all(z[i] == None for i in range(len(z))):
            return plotter.generate_plot2d(x, y, value, 'nome2d', 'titulo2d')
        else:
            #z = [z[i] = 0 for i in range(len(z)) if z[i] == None] ----------------------------------> testar
            
            return plotter.generate_plot3d(x, y, z, value+'3d', None, {'size': '10', 'opacity': '0.7'}, 'nome3d', 'titulo3d')

    else:
        return None
                      


if __name__ == '__main__':
    app.run_server(debug=True)
