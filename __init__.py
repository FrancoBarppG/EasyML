from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash import Dash

from apps.app_logged import *
from apps.app_notlogged import *
from libs import regs
from libs import plot_functions as plotter

import os
import time
import base64

from flask import Flask, render_template, flash, request, url_for, redirect
import sqlite3
from passlib.hash import sha256_crypt



users = sqlite3.connect(os.path.abspath('database/users.db'))

cursor = users.cursor()
#cursor.execute("""
#CREATE TABLE USERS(
#        username TEXT NOT NULL,
#        password TEXT NOT NULL,
#        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
#);
#""")
#cursor.execute("""
#CREATE TABLE DATATABLES(
#        path TEXT NOT NULL,
#        password TEXT NOT NULL,
#        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
#);
#""")


#cursor.execute("""
#INSERT INTO USERS (username, password)
#VALUES ('admin', 'admin')
#""")
#
#cursor.execute("""
#INSERT INTO USERS (username, password)
#VALUES ('franco', 'franco')
#""")
users.commit()
users.close()

server = Flask(__name__)

@server.route('/')
def index():
    return render_template('index.html')

@server.route('/<path:subpath>')
def index_2(subpath):
    return render_template('index.html')


app_logged = Dash(name='loggedapp', server=server)
app_logged.layout = app_logged_layout

@server.route('/notlogged/')
def notlogged():
    return app_notlogged.index()
app_notlogged = Dash(name='notloggedapp', url_base_pathname='/notlogged/', server=server)
app_notlogged.layout = app_notlogged_layout
#TODO colocar callbacks pro app_notlogged tb 




@server.route('/register/')
def register():
    return render_template('register.html')

@server.route('/logged/', methods=['GET', 'POST'])
def logged():
    if request.method == 'POST':
        username = request.form['username'].replace(' ','')
        password = request.form['password'].replace(' ','')
        
        users = sqlite3.connect(os.path.abspath('database/users.db'))
        cursor = users.cursor()

        insert = (username,)
        
        try:
            query = cursor.execute("""
            SELECT password FROM USERS
            WHERE username=?;""", insert)
            selection = query.fetchall()
            print(selection)

            users.close()
            if selection == []:
                return render_template('loginfailed.html')
            else:
                if sha256_crypt.verify(password, selection[0][0]):
                    return app_logged.index()
                else:
                    return render_template('loginfailed.html')
        except Exception as e:
            print(e)
            users.close()
            return render_template('loginfailed.html')
    elif request.method == 'GET':
        return redirect('login.html')
    else:
        return redirect('loginfailed.html')

@server.route('/loggedapp/')        
def loggedapp():
    return redirect('/logged/')

@server.route('/login/')
def login():
    return render_template('login.html')

@server.route('/deu_boa/', methods=['GET', 'POST'])
def deu_boa():
    if request.method == 'POST':
        username = request.form['username'].replace(' ','')
        password = request.form['password'].replace(' ','')

        insert = (username,password)

        users = sqlite3.connect(os.path.abspath('database/users.db'))
        cursor = users.cursor()

        if len(username.replace(' ', ''))<6 or len(password.replace(' ', ''))<6:
            return render_template('error.html')
        
        password = sha256_crypt.encrypt(password)

        try:
            insert = (username,) 
            query = cursor.execute("""
            SELECT * FROM USERS
            WHERE username=?""", insert)
            selection = query.fetchall()        
            print(selection)
            users.close()
            if selection != []:
                return render_template('registerunsuccessful.html')
            else:
                users = sqlite3.connect(os.path.abspath('database/users.db'))
                cursor = users.cursor()
                insert = (username, password)
                print('aaaaaaaaaaa')
                cursor.execute("""
                INSERT INTO USERS(username, password)
                VALUES(?,?)""", insert)
                users.commit()
                users.close()
                
                return render_template('deu_boa.html')
        except:
           return render_template('error.html') 
        





    



#===============================================================================
#=====================================CALLBACKS=================================
#===============================================================================
# Coloca o arquivo de upload na planilha
@app_logged.callback(Output('datatable', 'rows'),
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
@app_logged.callback(
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
@app_logged.callback(
    Output(component_id='size_bubble1_div', component_property='style'),
    [Input(component_id='type_marker1', component_property='value')])

def update_size_bubble1(mode1):
    if mode1 == 'markers':
        return None
    elif mode1 == 'lines' or mode1 == 'fill':
        return {'display': 'none'}

@app_logged.callback(
    Output(component_id='size_bubble2_div', component_property='style'),
    [Input(component_id='type_marker2', component_property='value')])

def update_size_bubble2(mode2):
    if mode2 == 'markers':
        return None
    elif mode2 == 'lines' or mode2 == 'fill':
        return {'display': 'none'}



#Se for colocado em 2d, vai automaticamente pra 'lines', se for 3d, vai automaticamente pra 'bubbles'
@app_logged.callback(
    Output(component_id='type_marker1', component_property='value'),
    [Input(component_id='type_dimensions', component_property='value')])

def to_bubble_1(dimensions):
    if dimensions == '3d':
        return 'bubbles'
    else:
        return 'lines'

@app_logged.callback(
    Output(component_id='type_marker2', component_property='value'),
    [Input(component_id='type_dimensions', component_property='value')])

def to_bubble_2(dimensions):
    if dimensions == '3d':
        return 'bubbles'
    else:
        return 'lines'

@app_logged.callback(
    Output(component_id='password_div', component_property='children'),
    [Input(component_id='datatable', component_property='rows'),
    Input(component_id='save_button', component_property='n_clicks'),
    Input(component_id='password_text', component_property='value')])

def save_table(rows, n_clicks, password):
    if n_clicks != None and password.replace(' ','') != '':

        for root, _, filenames in os.walk('/database/csv_files/'):
            if filename == password+'.csv':
                return html.H5('Essa senha já foi usada. Escolha outra senha')

        #Gera senha
        generated_password = sha256_crypt.encrypt(str(time.time())).replace('/', '')[17:22]
        csv_name = 'database/csv_files/{}.csv'.format(password)
        #Gera csv
        df = pandas.DataFrame(rows)
        df.to_csv(csv_name, encoding='utf-8', index=False)

        users = sqlite3.connect(os.path.abspath('database/users.db'))
        cursor = users.cursor()

        insert = (generated_password,)
        cursor.execute("""
        SELECT * FROM DATATABLES
        WHERE password=?""",insert)
        selection = cursor.fetchall() 


        if selection == []:
            insert = (csv_name,generated_password)
            cursor.execute("""
            INSERT INTO DATATABLES(path,password)
            VALUES(?,?)""",insert)
            users.commit()
            users.close()
            return html.H5('Datatable salva! Use essa senha para usar sua tabela novamente: {}'.format(generated_password))
            
        else:
            users.close()
            return html.H5('Error, please try again')


        

        
        
        
    
    

               
# Atualiza o gráfico de acordo com a planilha e os outros parâmetros
@app_logged.callback(
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


# Run the server
if __name__ == '__main__':
    server.run(debug=True, port=8050)
    
