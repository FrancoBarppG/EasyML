from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from dash import Dash

from flask import Flask

from app_logged import app_logged

import os

from dash_flask_login import FlaskLoginAuth
import sqlite3
import hashlib
from flask_login import UserMixin

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
