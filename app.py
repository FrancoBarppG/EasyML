import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as plotly
import plotly.graph_objs as plotly_go
from dash.dependencies import Input, Output
import dash_table_experiments as dt
import pandas
from flask import send_from_directory
import base64

app = dash.Dash()
server = app.server

N_TABLES = 100

app.scripts.config.serve_locally=True
app.css.config.serve_locally = True

######

def generate_plot2d(x_data, y_data, plot_type, plot_name, plot_title):
    return{'data': [
        {'x': x_data, 'y': y_data, 'type': plot_type, 'name': plot_name},
    ],
    'layout': {
        'title': plot_title
    }
    }



def generate_plot3d(x_data, y_data, z_data, plot_type, plot_text, marker_data,  plot_name, plot_title):

    return{'data': [
        {'x': x_data, 'y': y_data, 'z': z_data, 'type': plot_type, 'text': plot_text,
         'marker': marker_data, 'name': plot_name},
    ],
    'layout': {
        'title': plot_title
    }
    }

RECORDS = [
    {'X': '', 'Y': '', 'Z': ''}
    for i in range(N_TABLES)
]

#logo_img = 'logo.png'
#encoded_logo = base64.b64encode(open(logo_img, 'rb').read())

app.layout = html.Div(children = [

    #html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_logo))]),
    html.Div([html.Img(src='https://i.imgur.com/WXEV5Oo.png', style = {'width': '320px', 'height': '80px'})]),
    
    dcc.Tabs(id="tabs", vertical=False, children = [
        dcc.Tab(label = 'Graph', children = [

            html.Link(rel='stylesheet', href='/static/dash-datatable.css'),
            
            html.Div(children = dt.DataTable(
                rows = RECORDS,
                columns = ['X', 'Y', 'Z'],
                row_selectable = False,
                filterable = False,
                sortable = False,
                editable = True,
                id = 'datatable',
                max_rows_in_viewport = 10,
                

            ),

            className = 'container'
            ),

            dcc.Graph(id='output_graph', style = {'width': '100%', 'height': '100%', 'display': 'inline-block', 'borderLeft': '1px solid #d6d6d6', 'borderRight': '1px solid #d6d6d6', 'borderBottom': '1px solid #d6d6d6'}),

            html.Div([
                html.Div(id='content'),
                dcc.Location(id='location', refresh=False),
                html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
            

            ])
            ]),
        
        dcc.Tab(label = 'Config', children = [
            html.Div([
                html.H1("Alguma coisa")
                ])
            ])
        ],
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


@app.callback(
    Output(component_id='output_graph', component_property='figure'),
    [Input(component_id='datatable', component_property = 'rows')]
)

def update_figure(rows):
    dff = pandas.DataFrame(rows)
    x = dff['X']
    y = dff['Y']
    z = dff['Z']

    z_indices = []

    for i in range(N_TABLES):
        z_index = rows[i]['Z']
        if z_index=='':
            z_index = '0'
        z_indices.extend(z_index)
    
    
    #colocar 0 nos q n tem nada escrito qdo for gerar um 3d
    if all(z_indices[index] == '0' for index in range(N_TABLES)):
        return generate_plot2d(x, y, 'scatter', 'nome2d', 'titulo2d')
    else:
        return generate_plot3d(x, y, z_indices, 'scatter3d', None, {'size': '10', 'opacity': '0.7'}, 'nome3d', 'titulo3d')





if __name__ == '__main__':
    app.run_server(debug=True)
