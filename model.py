# http://www.capsunlock.net/2011/05/coding-with-flask-and-sqlalchemy.html
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float
import config

# DB class
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
db = SQLAlchemy(app)

# DB classes
class Blog(db.Model):
    __tablename__ = 'blog'

    def __init__(self):
        return;

    def __repr__(self):
        return 'Blablabla'