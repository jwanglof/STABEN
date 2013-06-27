#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from sqlalchemy import Table, Column, Integer, String, Date, Time, Text, create_engine
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Need this to make ImmutableMultiDict's that can be inserted into the database
from werkzeug.datastructures import ImmutableMultiDict

dbhost = '127.0.0.1'
dbuser = 'STABEN'
dbpass = 'generalhenrik'
dbname = 'STABEN'

# URI is needed for migrations
# We don't use this right now
# SQLALCHEMY_DATABASE_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname
# SQLALCHEMY_MIGRATE_REPO = 'db_repo'

engine = create_engine('mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

DEBUG = True
SECRET_KEY = ':\xbe\xef\xc9\xbf\xf6\x86\x8d\xeb\x90\xa5!+\x97i\xa38\xe0\x98\x7f\xec\xca*\x8c'
USERNAME = 'admin'
PASSWORD = 'default'

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

app = Flask(__name__)
app.secret_key = SECRET_KEY
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

user_roles = [u'Admin', u'Överfadder', u'Fadder', u'Klassföreståndare', u'Användare']

# TODO
# Fix DB migration!
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database