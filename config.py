from flask import Flask, request, session, g, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from sqlalchemy import Table, Column, Integer, String, Date, Time, Text, create_engine

dbhost = 'localhost'
dbuser = 'STABEN'
dbpass = 'generalhenrik'
dbname = 'STABEN'

SQLALCHEMY_DATABASE_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname
SQLALCHEMY_MIGRATE_REPO = 'db_repo'

DEBUG = True
SECRET_KEY = ':\xbe\xef\xc9\xbf\xf6\x86\x8d\xeb\x90\xa5!+\x97i\xa38\xe0\x98\x7f\xec\xca*\x8c'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# TODO
# Fix DB migration!
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database