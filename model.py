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
	"""Message of the Day-table

	Contains several messages that will be chosen randomly
	"""

	__tablename__ = 'motd'
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(100), index=True, unique=True)
	message = db.Column(db.String(254), index=True)
	show_on_date = db.Column(db.Date(), index=True, unique=True)

	def __init__(self, title=None, message=None, show_on_date=None):
		"""The constructor"""
		self.title = title
		self.message = message
		self.show_on_date = show_on_date

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return 'MOTD on date %i contains %s' % (self.show_on_date, self.message)

class Blog(db.Model):
	"""Blog-table

	Contains the blog entries
	"""
	
	__tablename__ = 'blog'
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(100), index=True, unique=False)
	text = db.Column(db.UnicodeText())
	date = db.Column(db.Date(), index=True, unique=True)
	time = db.Column(db.Time(), index=True)
	author = db.Column(db.String(40), index=True)
	blog_comments = db.relationship('blog_comments', uselist=False, backref='blog')

	def __init__(self, title=None, text=None, date=None, time=None, author=None):
		"""The constructor"""
		self.title = title
		self.text = text
		self.date = date
		self.time = time
		self.author = author

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return 'The blog %s has %s as author!' % (self.title, self.author)

class BlogComments(db.Model):
	"""Blog comments-table

	Contains the comments to a blog. Connected with Blog with fk_blog_id
	"""
	
	__tablename__ = 'blog_comments'
	id = db.Column(db.Integer(), primary_key=True)
	fk_blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
	comment = db.Column(db.String(250), index=True)
	date = db.Column(db.Date(), index=True)
	time = db.Column(db.Time(), index=True)
	author = db.Column(db.String(40), index=True)

	def __init__(self, belong_to_id=0, comment=None, date=None, time=None, author=None):
		"""The constructor"""
		self.belong_to_id = belong_to_id
		self.comment = comment
		self.date = date
		self.time = time
		self.author = author

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return 'The blog comment belongs to %i, was written by %s and contains %s' % (self.belong_to_id, self.author, self.comment)

'''
	Role will represent:
	* STABEN (admins)                          (ROLE_ADMIN)
	* Överfadder                               (role=1)
	* Fadder                                   (role=2)
	* Klassföreståndare                        (role=3)
	* Studievägledning                         (role=4)
	* Nollan                                   (ROLE_USER)
'''
class Users(db.Model):
	"""Users-table

	Contains all the registered users
	"""
	
	__tablename__ = 'users'
	id = db.Column(db.Integer(), primary_key=True)
	email = db.Column(db.String(100), index=True, unique=True)
	password = db.Column(db.String(50), index=True)
	role = db.Column(db.SmallInteger(), default=ROLE_USER)
	user_information = db.relationship('user_information', uselist=False, backref='users')

	def __init__(self, email=None, password=None, role=ROLE_USER):
		"""The constructor"""
		self.email = email
		self.password = password

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return 'Email %s has %s as role' % (self.email, self.role)

class UserInformation(db.Model):
	"""User information-table

	Contains a user's information. Connected with Users with fk_user_id
	"""
	
	__tablename__ = 'user_information'
	id = db.Column(db.Integer(), primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	title = db.Column(db.String(15), index=True, default='Användare')
	firstname = db.Column(db.String(100), index=True, default='')
	lastname = db.Column(db.String(100), index=True)
	phonenumber = db.Column(db.String(15), index=True)
	phonenumber_vis = db.Column(db.SmallInteger, index=True, default=0)
	age = db.Column(db.SmallInteger(), index=True)
	facebook_url = db.Column(db.String(100), index=True)
	school_class = db.Column(db.SmallInteger(), index=True)
	current_city = db.Column(db.String(100), index=True)
	where_from = db.Column(db.String(100), index=True)
	presentation = db.Column(db.UnicodeText())
	login_count = db.Column(db.Integer(), default=0)
	poll_done = db.Column(db.SmallInteger(), default=0)

	def __init__(self, firstname=None, user_id=None):
		"""The constructor"""
		self.user_id = user_id
		self.firstname = firstname

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return 'Hejsan %s' % (self.firstname)

class Contact(db.Model):
	"""Conact-table

	Contains the information for the school personnel that doesn't need a login.
	"""

	__tablename__ = 'contacts'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(30), index=True, unique=True)
	phone = db.Column(db.String(30), index=True)
	email = db.Column(db.String(100), index=True)
	#role determines if "klassföreståndare" or "studievägledning"
	#role = 0 "klassföreståndare, role = 1 "studievägledning"
	role = db.Column(db.SmallInteger)
	#In case of "klassföreståndare"
	school_class = db.Column(db.String(4), index=True)
	#In case of "studievägledning"
	link = db.Column(db.String(100), index=True)

	def __init__(self, name=None, phone=None, email=None, role=None, school_class=None, link=None):
		"""The constructor"""
		self.name = name
		self.phone = phone
		self.email = email
		self.role = role
		self.school_class = school_class
		self.link = link

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return 'Hejsan %s' % (self.firstname)

class SchoolClasses(db.Model):
	"""School classes-table

	Contains the school classes that the student can choose between when register
	"""
	
	__tablename__ = 'school_classes'
	id = db.Column(db.Integer(), primary_key=True)
	abbreviation = db.Column(db.String(5), index=True, unique=True)
	name = db.Column(db.String(100), index=True, unique=True)
	schedule = db.Column(db.String(254), index=True)

	def __init__(self, abbreviation=None, name=None, schedule=None):
		"""The constructor"""
		self.abbreviation = abbreviation
		self.name = name
		self.schedule = schedule

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return 'Bajs osv'

class RegisterCode(db.Model):
	"""Register code-table

	Contains the 'unique' code that are used on registration
	"""
	
	__tablename__ = 'register_code'
	id = db.Column(db.Integer(), primary_key=True)
	code = db.Column(db.String(10), index=True, unique=True)

	def __init__(self, code=None):
		"""The constructor"""
		self.code = code

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return 'Le kod iz: %s' % (self.code)

class ScheduleDate(db.Model):
	"""Schedule date-table

	Contains which weekday and what date a scheduled event is on
	"""
	
	__tablename__ = 'schedule_date'
	id = db.Column(db.Integer, primary_key=True)
	week = db.Column(db.Integer, index=True)
	date = db.Column(db.String(6), index=True, unique=True)
	weekday = db.Column(db.String(10), index=True)
	href_div_id = db.Column(db.String(4), index=True)
	img_url = db.Column(db.String(254), index=True)
	time = db.Column(db.String(20), index=True)
	place = db.Column(db.String(100), index=True)
	href_div_id = db.Column(db.String(4), index=True)
	# Two different for two paragrahps
	activity_info_day = db.Column(db.String(800), index=True)
	activity_info_evening = db.Column(db.String(800), index=True)

	def __init__(self, week=None, date=None, weekday=None, href_div_id=None,
				 img_url=None, time=None, place=None, activity_info_day=None, activity_info_evening=None):
		"""The constructor"""
		self.week = week
		self.date = date
		self.weekday = weekday
		self.href_div_id = href_div_id
		self.img_url = img_url
		self.time = time
		self.place = place
		self.activity_info_day = activity_info_day
		self.activity_info_evening = activity_info_evening
		return

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return;

class StudentPollResult(db.Model):
	"""Student poll result-table

	Contains the results the student had on the student poll. Connected with Users with fk_user_id
	"""
	
	__tablename__ = 'student_poll'
	id = db.Column(db.Integer, primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	dattamaskin(db.SmallInteger())
	# Will contain each answer for fk_user_id

	def __init__(self):
		"""The constructor"""
		return

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return;

class StudentPollQuestions(db.Model):
	"""Student poll questions-table

	Contains the questions for the student poll
	"""
	
	__tablename__ = 'student_poll_questions'
	id = db.Column(db.Integer, primary_key=True)
	group_name()
	real_question(String)
	dattamaskin(db.Integer)

	def __init__(self):
		"""The constructor"""
		return

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return;

class StudentRights(db.Model):
	"""Student rights-table

	Contains which student group the user is apart of. Connected with Users with fk_user_id and StudentGroups with fk_student_group
	"""
	
	__tablename__ = 'student_rights'
	fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	fk_student_group = db.Column(db.Integer, db.ForeignKey('studendgroups.id'))

	def __init__(self):
		"""The constructor"""
		return

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return;
	
class StudentGroups(db.Model):
	"""Student groups-table

	Contains what groups a user can be apart of
	"""
	
	__tablename__ = 'student_groups'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True, unique=True)

	def __init__(self):
		"""The constructor"""
		return

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return;

class Prices(db.Model):
	"""Prices-table

	Contains all the prices that are used
	"""
	
	__tablename__ = 'student_groups'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True, unique=True)
	information = db.Column(db.UnicodeText())
	price = db.Column(db.Integer)

	def __init__(self):
		"""The constructor"""
		return

	def __repr__(self):
		"""Get values from the table in an own-formatted output"""
		return;