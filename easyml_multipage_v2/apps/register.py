from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from dash import Dash

from apps.app_logged import app_logged

import os
import shutil

from flask import Flask
from dash_flask_login import FlaskLoginAuth
import dash_flask_login
import sqlite3
import hashlib
from flask_login import UserMixin

#Issue: https://github.com/gaw89/dash-flask-login/issues/6
#Troca o HTML padrão de login pelo especificado
##new = os.path.dirname(os.path.abspath(__file__)) + '/assets/login.html'
##print(new)
##old = os.path.dirname(dash_flask_login.__file__) + '/templates/default_login.html'
##shutil.copyfile(new, old)

users = sqlite3.connect(os.path.abspath('database/users.db'))

#cursor = users.cursor()
#cursor.execute("""
#CREATE TABLE USERS(
#        username TEXT NOT NULL,
#        password TEXT NOT NULL,
#        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
#);
#""")
#
#cursor.execute("""
#INSERT INTO USERS (username, password)
#VALUES ('admin', 'admin')
#""")
#
#cursor.execute("""
#INSERT INTO USERS (username, password)
#VALUES ('franco', 'franco')
#""")

#users.commit()

server = app_logged.server
auth = FlaskLoginAuth(app_logged, use_default_views=True, users=users)

users.close()

# Run the server
if __name__ == '__main__':
    server.run(debug=True, port=8050)
