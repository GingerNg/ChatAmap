# https://pythonbasics.org/flask-sqlalchemy/
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = None
db = None

def init_db_app(db_url, secret_key= "random string"):
    global app, db
    if app is None and db is None:
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        app.config['SECRET_KEY'] = secret_key

        db = SQLAlchemy(app)
    return db, app

