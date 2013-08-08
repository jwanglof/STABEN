#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail, Message
from sqlalchemy import Table, Column, Integer, String, Date, Time, Text, create_engine
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base

# Need this to make ImmutableMultiDict's that can be inserted into the database
from werkzeug.datastructures import ImmutableMultiDict, MultiDict, OrderedMultiDict

dbhost = '127.0.0.1'
dbuser = 'STABEN'
dbpass = 'generalhenrik'
dbname = 'STABEN'

# URI is needed for migrations
# We don't use this right now
# SQLALCHEMY_DATABASE_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname
# SQLALCHEMY_MIGRATE_REPO = 'db_repo'

engine = create_engine('mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

DEBUG = False
SECRET_KEY = ':\xbe\xef\xc9\xbf\xf6\x86\x8d\xeb\x90\xa5!+\x97i\xa38\xe0\x98\x7f\xec\xca*\x8c'
USERNAME = 'admin'
PASSWORD = 'default'
HOST = '0.0.0.0'

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config.setdefault('MAIL_SERVER', 'smtp.gmail.com')
app.config.setdefault('MAIL_PORT', 465)
# app.config.setdefault('MAIL_USE_TSL', True)
app.config.setdefault('MAIL_USE_SSL', True)
# app.config.setdefault('MAIL_USERNAME', 'c30g@c.lintek.liu.se')
# app.config.setdefault('MAIL_PASSWORD', 'WpD0cJhwQj2')
app.config.setdefault('MAIL_USERNAME', 'staben.no.reply@gmail.com')
app.config.setdefault('MAIL_PASSWORD', 'zFpgai3g')
app.config.setdefault('MAIL_DEFAULT_SENDER', ('STABENs ultimata epost no-reply e-post', 'staben.no.reply@gmail.com'))
mail = Mail(app)

user_roles = [u'Admin', u'Överfadder', u'Fadder', u'Klassföreståndare', u'Användare']

# TODO
# Fix DB migration!
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database