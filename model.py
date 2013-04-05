#!/usr/bin/python
# -*- coding: utf-8 -*-

# http://www.capsunlock.net/2011/05/coding-with-flask-and-sqlalchemy.html
# Why UNIQUE=TRUE: http://stackoverflow.com/questions/707874/differences-between-index-primary-unique-fulltext-in-mysql
# 

'''
To clear users and userInformation
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE users;
TRUNCATE userInformation;
SET FOREIGN_KEY_CHECKS=1;
'''

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
    * STABEN (admins)                          (ROLE_ADMIN)
    * Överfadder                               (role=1)
    * Fadder                                   (role=2)
    * Klassföreståndare                        (role=3)
    * Användare                                (ROLE_USER)
'''
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(50), index=True)
    role = db.Column(db.SmallInteger(), default=ROLE_USER)
    information = db.relationship('UserInformation', uselist=False, backref='users')

    def __init__(self, email=None, password=None, role=ROLE_USER):
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return 'Email %s has %s as role' % (self.email, self.role)

class UserInformation(db.Model):
    __tablename__ = 'userInformation'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(15), index=True)
    firstname = db.Column(db.String(100), index=True)
    lastname = db.Column(db.String(100), index=True)
    phonenumber = db.Column(db.String(15), index=True)
    phonenumber_vis = db.Column(db.SmallInteger, index=True, default=0)
    age = db.Column(db.SmallInteger(), index=True)
    facebook_url = db.Column(db.String(100), index=True)
    school_class = db.Column(db.SmallInteger(), index=True)
    current_city = db.Column(db.String(100), index=True)
    where_from = db.Column(db.String(100), index=True)
    presentation = db.Column(db.UnicodeText())
    times_signed_in = db.Column(db.Integer(), default=0)

    def __init__(self, firstname=None):
        self.firstname = firstname

    def __repr__(self):
        return 'Hejsan %s' % (self.firstname)

class SchoolClasses(db.Model):
    __tablename__ = 'school_classes'
    id = db.Column(db.Integer(), primary_key=True)
    abbreviation = db.Column(db.String(5), index=True, unique=True)
    name = db.Column(db.String(100), index=True, unique=True)
    schedule = db.Column(db.String(254), index=True)

    def __init__(self, abbreviation=None, name=None, schedule=None):
        self.abbreviation = abbreviation
        self.name = name
        self.schedule = schedule

    def __repr__(self):
        return 'Bajs osv'

'''class StudentPoll(db.Model):
    __tablename__ = 'student_poll'
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        return

    def __repr__(self):
        return;'''
