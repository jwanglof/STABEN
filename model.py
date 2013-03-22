#!/usr/bin/python
# -*- coding: utf-8 -*-

# http://www.capsunlock.net/2011/05/coding-with-flask-and-sqlalchemy.html
# Why UNIQUE=TRUE: http://stackoverflow.com/questions/707874/differences-between-index-primary-unique-fulltext-in-mysql
# 

'''
* IMPORTANT!
* The database MUST be created before the script can create the models!
'''

import config

# Defines
ROLE_ADMIN = 0
ROLE_USER = 9

db = config.db
app = config.app

# DB classes
class Motd(db.Model):
    __tablename__ = 'motd'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    message = db.Column(db.String(254), index=True)
    show_on_date = db.Column(db.Date(), index=True, unique=True)

    def __init__(self, title=None, message=None, show_on_date=None):
        self.title = title
        self.message = message
        self.show_on_date = show_on_date

    def __repr__(self):
        return 'MOTD on date %i contains %s' % (self.show_on_date, self.message)

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), index=True, unique=False)
    text = db.Column(db.UnicodeText())
    date = db.Column(db.Date(), index=True, unique=True)
    time = db.Column(db.Time(), index=True)
    author = db.Column(db.String(40), index=True)

    def __init__(self, title=None, text=None, date=None, time=None, author=None):
        self.title = title
        self.text = text
        self.date = date
        self.time = time
        self.author = author

    def __repr__(self):
        return 'The blog %s has %s as author!' % (self.title, self.author)

class BlogComments(db.Model):
    __tablename__ = 'blog_comments'
    id = db.Column(db.Integer(), primary_key=True)
    belong_to_id = db.Column(db.Integer(), index=True, unique=True)
    comment = db.Column(db.String(250), index=True)
    date = db.Column(db.Date(), index=True)
    time = db.Column(db.Time(), index=True)
    author = db.Column(db.String(40), index=True)

    def __init__(self, belong_to_id=0, comment=None, date=None, time=None, author=None):
        self.belong_to_id = belong_to_id
        self.comment = comment
        self.date = date
        self.time = time
        self.author = author

    def __repr__(self):
        return 'The blog comment belongs to %i, was written by %s and contains %s' % (self.belong_to_id, self.author, self.comment)

'''
    Users will represent:
    * STABEN (admins)                                  (role=0)
    * Överfadder                                         (role=1)
    * Fadder                                                    (role=2)
    * Klassföreståndare                              (role=3)
    * Användare                                                        (role=4)
'''
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(50), index=True)
    title = db.Column(db.String(15), index=True)
    role = db.Column(db.SmallInteger(), default=4)
    #information = db.relationship('UserInformation', backref='users', lazy='dynamic')
    firstname = db.Column(db.String(100), index=True)
    lastname = db.Column(db.String(100), index=True)
    phonenumber = db.Column(db.String(15), index=True)
    age = db.Column(db.Integer(3), index=True)
    facebook_link = db.Column(db.String(100), index=True)
    school_class = db.Column(db.String(15), index=True)
    current_city = db.Column(db.String(100), index=True)
    where_from = db.Column(db.String(100), index=True)
    times_signed_in = db.Column(db.Integer(), default=0)

    def __init__(self, email=None, password=None, title=None, role=3, firstname=None, lastname=None, phonenumber=None):
        self.email = email
        self.password = password
        self.title = title
        self.role = role
        self.firstname = firstname
        self.lastname = lastname
        self.phonenumber = phonenumber

    def __repr__(self):
        return 'The user named %s %s has title %s' % (self.firstname, self.lastname, self.title)

'''class UserInformation(db.Model):
    __tablename__ = 'userInformation'
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(100), index=True)
    lastname = db.Column(db.String(100), index=True)
    phonenumber = db.Column(db.String(15), index=True)
    age = db.Column(db.Integer(3), index=True)
    facebook_link = db.Column(db.String(100), index=True)
    school_class = db.Column(db.String(15), index=True)
    current_city = db.Column(db.String(100), index=True)
    where_from = db.Column(db.String(100), index=True)
    times_signed_in = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, firstname=None):
        self.firstname = firstname'''

'''class StudentPoll(db.Model):
    __tablename__ = 'student_poll'
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        return

    def __repr__(self):
        return;'''
