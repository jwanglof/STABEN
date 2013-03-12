from flask import Flask, request, session, g, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Time, Text, create_engine

dbhost = 'localhost'
dbuser = 'STABEN'
dbpass = 'generalhenrik'
dbname = 'STABEN'

SQLALCHEMY_DATABASE_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname
SQLALCHEMY_MIGRATE_REPO = 'db_repository'

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
