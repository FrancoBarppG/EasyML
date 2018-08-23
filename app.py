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

app = dash.Dash()
server = app.server

N_TABLES = 100

app.scripts.config.serve_locally=True
app.css.config.serve_locally = True
#app.config['suppress_callback_exceptions'] = True




@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


app.css.append_css({"external_url": "/static/{}".format('style.css')})
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


def generate_plot2d(x_data, y_data, plot_type, plot_name, plot_title):
    return{'data': [
        {'x': x_data, 'y': y_data, 'type': plot_type, 'name': plot_name},
    ],
    'layout': {
        'title': plot_title
    }
    }

def generate_plot2d_2(x_data, y_data, plot_type, plot_name, plot_title, x_data2, y_data2, plot_type2, plot_name2):
    return{'data': [
        {'x': x_data, 'y': y_data, 'type': plot_type, 'name': plot_name},
        {'x': x_data2, 'y': y_data2, 'type': plot_type2, 'name': plot_name2}
    ],
    'layout': {
        'title': plot_title
    }
    }



def generate_plot3d(x_data, y_data, z_data, plot_type, plot_text, marker_data,  plot_name, plot_title):

    return{'data': [
        {'x': x_data, 'y': y_data, 'z': z_data, 'type': plot_type, 'text': plot_text, 'marker': marker_data, 'name': plot_name},
    ],
    'layout': {
        'title': plot_title
    }
    }

def generate_plot3d_2(x_data, y_data, z_data, plot_type, plot_text, marker_data,  plot_name, plot_title, x_data2, y_data2, z_data2, plot_type2, plot_text2, marker_data2,  plot_name2, plot_title2):

    return{'data': [
        {'x': x_data, 'y': y_data, 'z': z_data, 'type': plot_type, 'text': plot_text, 'marker': marker_data, 'name': plot_name},
        {'x': x_data2, 'y': y_data2, 'z': z_data2, 'type': plot_type2, 'text': plot_text2, 'marker': marker_data2, 'name': plot_name2}
    ],
    'layout': {
        'title': plot_title
    }
    }


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

RECORDS = [
    {'X': '', 'Y': '', 'Z': ''}
    for i in range(N_TABLES)
]

#logo_img = 'logo.png'
#encoded_logo = base64.b64encode(open(logo_img, 'rb').read())

app.layout = html.Div(children = [

    #html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_logo))]),
    html.Div(id='header_img', style = {'width': '320px', 'height': '80px'}),
    
    dcc.Tabs(id='tabs', vertical=False, children = [
        dcc.Tab(label = 'Graph', children = [

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
                        'width': '100%',
                        'height': '60px',
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

            html.Button(id='reg_button', style = {'borderBottom': '2px solid #d6d6d6'}, children= [html.H3('Botão Regs')]),

            html.Div([
                html.Div(id='content'),
                dcc.Location(id='location', refresh=False),
                html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
            

            ])
            ]),
        
        dcc.Tab(label = 'Config', children = [
            html.Div([
                html.H1('Alguma coisa')
                ]),
            html.H3('Tipo do gráfico 2d'),
            html.Br(),
            dcc.Dropdown(
                options = [
                    {'label': 'Scatter', 'value': 'scatter'},
                    {'label': 'opcao 2', 'value': 'opcao2'},
                    {'label': 'opcao 3', 'value': 'opcao3'},
                    ],
                value = 'tipo2d',),
            html.H3('Tipo do gráfico 3d'),
            html.Br(),
            dcc.Dropdown(
                options = [
                    {'label': 'Scatter 3d', 'value': 'scatter3d'},
                    {'label': 'opcao 2', 'value': 'opcao2'},
                    {'label': 'opcao 3', 'value': 'opcao3'},
                    ],
                value = 'tipo3d',),
            html.Br(),
            html.Br(),
            html.Hr(),
            html.Br(),
            html.H3('Parâmetro 1'),
            html.Br(),
            dcc.Slider(
                min = 0,
                max = 9,
                marks = {i: '{}'.format(i) for i in range(10)},
                value = 5,
            ),
            html.Br(),
            html.H3('Parâmetro 2'),
            html.Br(),
            dcc.Slider(
                min = 0,
                max = 9,
                marks = {i: '{}'.format(i) for i in range(10)},
                value = 5,
            ),
            html.Br(),
            html.H3('Parâmetro 3'),
            html.Br(),
            dcc.Slider(
                min = 0,
                max = 9,
                marks = {i: '{}'.format(i) for i in range(10)},
                value = 5,
            )
        ])],
                
             style={
                'fontFamily': 'system-ui'
            },
                content_style={
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'borderBottom': '1px solid #d6d6d6',
                'padding': '44px'
            },
                parent_style={
                'maxWidth': '1000px',
                'margin': '0 auto'
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
     Input(component_id='datatable', component_property='rows')])

def update_figure(n_clicks, rows):
    
    if n_clicks is not None and len(rows[0]) is not 0:

        # Se tiver clickado uma vez, vai fazer a reg e atualizar o grafico

        dff = pandas.DataFrame(rows)

        x = dff['X']
        y = dff['Y']
        z = dff['Z']

        b,a = regs.least_squares(x,y) ####################################### lembrar de colocar opcao pra escolher

        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print(a)
        print(b)
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        x_2 = [i for i in range(int(max(x)))]
        y_2 = [(a*x_2[i] + b) for i in range(max(x))]
        

        if len(z)==0 or all(z[i] == None for i in range(len(z))):
            return generate_plot2d_2(x, y, 'scatter', 'nome2d', 'titulo2d', x_2, y_2, 'scatter', 'nome2d2')
        else:
            return generate_plot3d(x, y, z, 'scatter3d', None, {'size': '10', 'opacity': '0.7'}, 'nome3d', 'titulo3d')


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
            return generate_plot2d(x, y, 'scatter', 'nome2d', 'titulo2d')
        else:
            #z = [z[i] = 0 for i in range(len(z)) if z[i] == None] ----------------------------------> testar
            
            return generate_plot3d(x, y, z, 'scatter3d', None, {'size': '10', 'opacity': '0.7'}, 'nome3d', 'titulo3d')

    else:
        return None
                      


if __name__ == '__main__':
    app.run_server(debug=True)
