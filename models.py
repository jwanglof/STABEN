#!/usr/bin/python
# -*- coding: utf-8 -*-

# http://www.capsunlock.net/2011/05/coding-with-flask-and-sqlalchemy.html
# Why UNIQUE=TRUE: http://stackoverflow.com/questions/707874/differences-between-index-primary-unique-fulltext-in-mysql
# 

'''
To be able to delete all tables
SET FOREIGN_KEY_CHECKS=0;TRUNCATE users;TRUNCATE student_poll_prefix;TRUNCATE student_poll_question;TRUNCATE student_poll_answer;SET FOREIGN_KEY_CHECKS=1;
SET FOREIGN_KEY_CHECKS=0;TRUNCATE student_poll_prefix;TRUNCATE student_poll_question;TRUNCATE student_poll_answer;SET FOREIGN_KEY_CHECKS=1;
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
Base = config.Base

class Blog(Base):
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

	def __init__(self, title=None, text=None, date=None, time=None, author=None):
		"""The constructor"""
		self.title = title
		self.text = text
		self.date = date
		self.time = time
		self.author = author

class BlogComments(Base):
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

class Contacts(Base):
	"""Conacts-table

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

class Motd(Base):
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

class Prices(Base):
	"""Prices-table

	Contains all the prices that are used
	"""
	
	__tablename__ = 'prices'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True, unique=True)
	information = db.Column(db.UnicodeText())
	price = db.Column(db.Integer)

	def __init__(self):
		"""The constructor"""
		return

class RegisterCode(Base):
	"""Register code-table

	Contains the 'unique' code that are used on registration
	"""
	
	__tablename__ = 'register_code'
	id = db.Column(db.Integer(), primary_key=True)
	code = db.Column(db.String(10), index=True, unique=True)

	def __init__(self, code=None):
		"""The constructor"""
		self.code = code

class Schedule(Base):
	"""Schedule date-table

	Contains which weekday and what date a scheduled event is on
	"""
	
	__tablename__ = 'schedule'
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

class SchoolClass(Base):
	__tablename__ = 'school_class'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(100), index=True, unique=True)
	schedule = db.Column(db.String(254), index=True)
	fk_school_program_id = db.Column(db.Integer(), db.ForeignKey('school_program.id'))

	def __init__(self, name=None, schedule=None, fk_school_program_id=None):
		"""The constructor"""
		self.name = name
		self.schedule = schedule
		self.fk_school_program_id = fk_school_program_id

class SchoolProgram(Base):
	"""School classes-table

	Contains the school classes that the student can choose between when register
	"""
	
	__tablename__ = 'school_program'
	id = db.Column(db.Integer(), primary_key=True)
	abbreviation = db.Column(db.String(5), index=True, unique=True)
	name = db.Column(db.String(100), index=True, unique=True)
	r_school_class = db.relationship('SchoolClass', backref='SchoolProgram')

	def __init__(self, id=None, abbreviation=None, name=None):
		"""The constructor"""
		self.id = id
		self.abbreviation = abbreviation
		self.name = name

class StudentPollAnswer(Base):
	__tablename__ = 'student_poll_answer'
	id = db.Column(db.Integer, primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	fk_student_poll_question_id = db.Column(db.Integer, db.ForeignKey('student_poll_question.id'))

	# This will return the question id as an int instead of a
	# StudentPollAnswer object.
	# Need this to check the MultiDict in profile_student_poll
	def __int__(self):
		return self.fk_student_poll_question_id

	def __init__(self, fk_user_id=None, fk_student_poll_question_id=None):
		"""The constructor"""
		self.fk_user_id = fk_user_id
		self.fk_student_poll_question_id = fk_student_poll_question_id
		return

class StudentPollDialect(Base):
	__tablename__ = 'student_poll_dialect'
	id = db.Column(db.Integer, primary_key=True)
	dialect = db.Column(db.String(100), index=True, unique=True)
	max_students = db.Column(db.Integer(), default=0)
	r_student_poll_point = db.relationship('StudentPollPoint', backref='StudentPollDialect')
	r_student_poll_assigned_group = db.relationship('StudentPollAssignedGroups', backref='StudentPollDialect')

	def __init__(self, id=None, dialect=None):
		"""The constructor"""
		self.id = id
		self.dialect = dialect
		return

class StudentPollPoint(Base):
	__tablename__ = 'student_poll_point'
	id = db.Column(db.Integer, primary_key=True)
	fk_student_poll_dialect_id = db.Column(db.Integer, db.ForeignKey('student_poll_dialect.id'))
	fk_student_poll_question_id = db.Column(db.Integer, db.ForeignKey('student_poll_question.id'))
	point = db.Column(db.Integer)

	def __init__(self, fk_student_poll_dialect_id=None, fk_student_poll_question_id=None, point=None):
		"""The constructor"""
		self.fk_student_poll_dialect_id = fk_student_poll_dialect_id
		self.fk_student_poll_question_id = fk_student_poll_question_id
		self.point = point
		return

class StudentPollPrefix(Base):
	__tablename__ = 'student_poll_prefix'
	id = db.Column(db.Integer, primary_key=True)
	prefix = db.Column(db.String(100), index=True, unique=True)
	question = db.relationship('StudentPollQuestion', backref='StudentPollPrefix', lazy='joined')

	def __init__(self, id=None, prefix=None):
		"""The constructor"""
		self.id = id
		self.prefix = prefix
		return

class StudentPollQuestion(Base):
	__tablename__ = 'student_poll_question'
	id = db.Column(db.Integer, primary_key=True)
	fk_student_poll_prefix_id = db.Column(db.Integer, db.ForeignKey('student_poll_prefix.id'))
	question = db.Column(db.String(100), index=True)
	question_point = db.relationship('StudentPollPoint', backref='StudentPollQuestion', lazy='joined')

	def __init__(self, student_poll_prefix_id=None, question=None):
		"""The constructor"""
		self.fk_student_poll_prefix_id = student_poll_prefix_id
		self.question = question
		return

'''
	Role will represent:
	* STABEN (admins)                          (ROLE_ADMIN)
	* Överfadder                               (role=1)
	* Fadder                                   (role=2)
	* Klassföreståndare                        (role=3)
	* Studievägledning                         (role=4)
	* Gallerinollan							   (role=5)
	* Bloggnollan							   (role=6)
	* Nollan                                   (ROLE_USER)
'''
class Users(Base):
	"""Users-table

	Contains all the registered users
	"""
	
	__tablename__ = 'users'
	id = db.Column(db.Integer(), primary_key=True)
	email = db.Column(db.String(100), index=True, unique=True)
	password = db.Column(db.String(254), index=True)
	role = db.Column(db.SmallInteger(), default=ROLE_USER)
	user_information = db.relationship('UserInformation', backref='Users', uselist=False)
	student_poll = db.relationship('StudentPollAnswer', backref='Users', lazy='dynamic')
	r_student_poll_assigned_group = db.relationship('StudentPollAssignedGroups', backref='Users')

	def __init__(self, email=None, password=None, role=ROLE_USER):
		"""The constructor"""
		self.email = email
		self.password = password
		self.role = role

class UserInformation(Base):
	"""User information-table

	Contains a user's information. Connected with Users with fk_user_id
	"""
	
	__tablename__ = 'user_information'
	id = db.Column(db.Integer(), primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	firstname = db.Column(db.String(100), index=True, default='')
	lastname = db.Column(db.String(100), index=True, default='')
	allergies = db.Column(db.String(254), index=True, default='')
	food_preference = db.Column(db.SmallInteger(), index=True, default=0)
	phonenumber = db.Column(db.String(15), index=True, default='')
	phonenumber_vis = db.Column(db.SmallInteger, index=True, default=0)
	facebook_url = db.Column(db.String(100), index=True, default='')
	school_class = db.Column(db.SmallInteger(), index=True, default=1)
	current_city = db.Column(db.String(100), index=True, default='')
	where_from = db.Column(db.String(100), index=True, default='')
	presentation = db.Column(db.UnicodeText())
	login_count = db.Column(db.Integer(), default=0)
	poll_done = db.Column(db.SmallInteger(), default=0)
	finished_profile = db.Column(db.SmallInteger(), default=0)
	fk_student_dialect = db.Column(db.Integer, db.ForeignKey('student_poll_dialect.id'))

	def __init__(self, user_id=None, presentation=None):
		"""The constructor"""
		self.fk_user_id = user_id
		self.presentation = presentation

class StudentPollAssignedGroups(Base):
	__tablename__ = 'student_poll_assigned_groups'
	id = db.Column(db.Integer(), primary_key=True)
	fk_student_poll_dialect_id = db.Column(db.Integer, db.ForeignKey('student_poll_dialect.id'))
	fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	position = db.Column(db.Integer())

	def __init__(self, fk_student_poll_dialect_id=None, fk_user_id=None, position=None):
		"""The constructor"""
		self.fk_student_poll_dialect_id = fk_student_poll_dialect_id
		self.fk_user_id = fk_user_id
		self.position = position
