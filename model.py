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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    message = db.Column(db.String(254), index=True, unique=True)
    show_on_date = db.Column(db.Date, index=True, unique=True)

    def __init__(self, title=None, message=None, show_on_date=None):
        self.title = title
        self.message = message
        self.show_on_date = show_on_date

    def __repr__(self):
        return 'MOTD on date %i contains %s' % (self.show_on_date, self.message)

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    text = db.Column(db.Text, index=True, unique=True)
    date = db.Column(db.Date, index=True, unique=True)
    time = db.Column(db.Time, index=True, unique=True)
    author = db.Column(db.String(40), index=True, unique=True)

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
    id = db.Column(db.Integer, primary_key=True)
    belong_to_id = db.Column(db.Integer, index=True, unique=False)
    comment = db.Column(db.String(250), index=True, unique=True)
    date = db.Column(db.Date, index=True, unique=True)
    time = db.Column(db.Time, index=True, unique=True)
    author = db.Column(db.String(40), index=True, unique=True)

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
    * STABEN (admins)                                  (role=1)
    * Faddrar (Oeverfaddrar, Faddrar)       (role=2)
    * Klassfoerestandare                                (role=3)
    * Andra                                                        (role=4)
'''
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    firstname = db.Column(db.String(100), index=True, unique=True)
    lastname = db.Column(db.String(100), index=True, unique=True)
    title = db.Column(db.String(15), index=True, unique=True)
    #phonenumber = db.Column(db.Integer, index=True, unique=True)
    phonenumber = db.Column(db.String(15), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=3)

    def __init__(self, email=None, firstname=None, lastname=None, title=None, phonenumber=None, role=3):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.title = title
        self.phonenumber = phonenumber
        self.role = role

    def __repr__(self):
        return 'The user named %s %s has title %s' % (self.firstname, self.lastname, self.title)

waeggen_user = Users('jwanglof@gmail.com', 'Johan', 'Wanglof', 'WebmastAH', '0046708601911', 1)
simba_user = Users('simis.linden@gmail.com', 'Simon', 'Linden', 'WebmastAH', '0046735026994', 1)

'''class StudentPoll(db.Model):
    __tablename__ = 'student_poll'
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        return

    def __repr__(self):
        return;'''
