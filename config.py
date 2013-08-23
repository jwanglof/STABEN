#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail, Message
from sqlalchemy import Table, Column, Integer, String, Date, Time, Text, create_engine, asc, desc
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from dev import host_option

# Need this to make ImmutableMultiDict's that can be inserted into the database
from werkzeug.datastructures import ImmutableMultiDict, MultiDict, OrderedMultiDict

engine = create_engine('mysql://' + host_option.dbuser + ':' + host_option.dbpass + '@' + host_option.dbhost + '/' + host_option.dbname + '?charset=utf8', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

SECRET_KEY = ':\xbe\xef\xc9\xbf\xf6\x86\x8d\xeb\x90\xa5!+\x97i\xa38\xe0\x98\x7f\xec\xca*\x8c'
USERNAME = 'admin'
PASSWORD = 'default'

UPLOAD_FOLDER = host_option.root_path + '/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = SECRET_KEY
# app.debug = DEBUG
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config.setdefault('MAIL_SERVER', 'smtp.gmail.com')
app.config.setdefault('MAIL_PORT', 465)
# app.config.setdefault('MAIL_USE_TSL', True)
app.config.setdefault('MAIL_USE_SSL', True)
app.config.setdefault('MAIL_USERNAME', 'staben.no.reply@gmail.com')
app.config.setdefault('MAIL_PASSWORD', 'zFpgai3g')
app.config.setdefault('MAIL_DEFAULT_SENDER', ('STABENs ultimata epost no-reply e-post', 'staben.no.reply@gmail.com'))
mail = Mail(app)

user_roles = [u'Admin', u'Överfadder', u'Fadder', u'Klassföreståndare', u'Användare']