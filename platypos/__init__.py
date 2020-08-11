from flask import Flask

# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# La password è quella che chiede quando si installa postgres, mettere "passwordsupersegreta" per facilitare lo sviluppo
# "platypos_airlines" è il nome del db da creare da shell o pgadmin4
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:passwordsupersegreta@localhost:5432/platypos_airlines'
# db = SQLAlchemy(app)

import platypos.routes
