#!/usr/bin/python
# -*- coding: utf-8 -*-

# http://www.capsunlock.net/2011/05/coding-with-flask-and-sqlalchemy.html
# Why UNIQUE=TRUE: http://stackoverflow.com/questions/707874/differences-between-index-primary-unique-fulltext-in-mysql
# 

'''
To be able to delete all tables
SET FOREIGN_KEY_CHECKS=0;TRUNCATE user;TRUNCATE student_poll_prefix;TRUNCATE student_poll_question;TRUNCATE student_poll_answer;SET FOREIGN_KEY_CHECKS=1;
SET FOREIGN_KEY_CHECKS=0;TRUNCATE student_poll_prefix;TRUNCATE student_poll_question;TRUNCATE student_poll_answer;SET FOREIGN_KEY_CHECKS=1;
'''

'''
Role will represent:
* STABEN (admins)			(ROLE_ADMIN)
* Överfadder				(role=1)
* Fadder					(role=2)
* Klassföreståndare 		(role=3)
* Studievägledning 			(role=4)
* Gallerinollan 				(role=5)
* Bloggnollan 				(role=6)
* Nollan 					(ROLE_USER)
'''

'''
* IMPORTANT!
* The database MUST be created before the script can create the models!
'''

import config

# ROLES
ROLE_ADMIN 	= 0
ROLE_USER 	= 9

db = config.db
app = config.app
Base = config.Base

## Blog-table
# 
# Contains the blog entries
class Blog(Base):
	__tablename__ = 'blog'
	id = db.Column(db.Integer(), primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	fk_gallery_album_id = db.Column(db.Integer(), db.ForeignKey('gallery_album.id'), default=0)
	title = db.Column(db.String(100), index=True, unique=False)
	text = db.Column(db.UnicodeText())
	date = db.Column(db.Date(), index=True, unique=True)
	time = db.Column(db.Time(), index=True)
	r_blog_comment = db.relationship('BlogComment', backref='Blog')

	## The constructor
	def __init__(self, fk_user_id=None, fk_gallery_album_id=None, title=None, text=None, date=None, time=None):
		self.fk_user_id = fk_user_id
		self.fk_gallery_album_id = fk_gallery_album_id
		self.title = title
		self.text = text
		self.date = date
		self.time = time

## Blog comments-table
#
# Contains the comments to a blog. Connected with Blog with fk_blog_id
class BlogComment(Base):
	__tablename__ = 'blog_comment'
	id = db.Column(db.Integer(), primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	fk_blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
	comment = db.Column(db.String(250), index=True)
	date = db.Column(db.Date(), index=True)
	time = db.Column(db.Time(), index=True)

	## The constructor
	def __init__(self, fk_user_id=None, fk_blog_id=None, comment=None, date=None, time=None):
		self.fk_user_id = fk_user_id
		self.fk_blog_id = fk_blog_id
		self.comment = comment
		self.date = date
		self.time = time

## Contact-table
#
# Contains the information for the school personnel that doesn't need a login.
class Contact(Base):
	__tablename__ = 'contact'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(30), index=True, unique=True)
	phone = db.Column(db.String(30), index=True)
	email = db.Column(db.String(100), index=True)

	## role determines if the added contact is "klassföreståndare" or "studievägledning".
	## role = 0 "klassföreståndare, role = 1 "studievägledning"
	role = db.Column(db.SmallInteger)

	## In case of "klassföreståndare"
	school_class = db.Column(db.String(4), index=True)

	## In case of "studievägledning"
	link = db.Column(db.String(100), index=True)

	## The constructor
	def __init__(self, name=None, phone=None, email=None, role=None, school_class=None, link=None):
		self.name = name
		self.phone = phone
		self.email = email
		self.role = role
		self.school_class = school_class
		self.link = link

## Gallery albums-table
#
# Contains all the gallery albums created
class GalleryAlbum(Base):
	__tablename__ = 'gallery_album'
	id = db.Column(db.Integer(), primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	date = db.Column(db.Date(), index=True)
	time = db.Column(db.Time(), index=True)
	title = db.Column(db.String(100), index=True)
	description = db.Column(db.String(200), index=True)
	approved = db.Column(db.SmallInteger(), default=0)
	r_gallery_picture = db.relationship('GalleryPicture', backref='GalleryAlbum')
	r_gallery_comment = db.relationship('GalleryComment', backref='GalleryAlbum')
	r_blog = db.relationship('Blog', backref='GalleryAlbum')

	## The constructor
	def __init__(self, fk_user_id=None, date=None, time=None, title=None, description=None, approved=0):
		self.fk_user_id = fk_user_id
		self.date = date
		self.time = time
		self.title = title
		self.description = description
		self.approved = approved

## Gallery pictures-table
#
# Contains all the pictures in the galleries
class GalleryPicture(Base):
	__tablename__ = 'gallery_picture'
	id = db.Column(db.Integer(), primary_key=True)
	fk_user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	fk_gallery_album_id = db.Column(db.Integer(), db.ForeignKey('gallery_album.id'))
	description = db.Column(db.String(200), index=True)
	date = db.Column(db.Date(), index=True)
	time = db.Column(db.Time(), index=True)
	path = db.Column(db.String(254), index=True)

	## The constructor
	def __init__(self, fk_user_id=None, fk_gallery_album_id=None, date=None, time=None, path=None, description=None):
		self.fk_user_id = fk_user_id
		self.fk_gallery_album_id = fk_gallery_album_id
		self.date = date
		self.time = time
		self.path = path
		self.description = description

## Gallery comment-table
#
# Contains all the gallery comments
class GalleryComment(Base):
	__tablename__ = 'gallery_comment'
	id = db.Column(db.Integer(), primary_key=True)
	fk_user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	fk_gallery_album_id = db.Column(db.Integer(), db.ForeignKey('gallery_album.id'))
	comment = db.Column(db.String(254), index=True)
	date = db.Column(db.Date(), index=True)
	time = db.Column(db.Time(), index=True)

	## The constructor
	def __init__(self, fk_user_id=None, fk_gallery_album_id=None, comment=None, date=None, time=None):
		self.fk_user_id = fk_user_id
		self.fk_gallery_album_id = fk_gallery_album_id
		self.comment = comment
		self.date = date
		self.time = time

## Message of the Day-table
#
# Contains several messages that will be chosen randomly
class Motd(Base):
	__tablename__ = 'motd'
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(100), index=True, unique=True)
	message = db.Column(db.String(254), index=True)
	show_on_date = db.Column(db.Date(), index=True, unique=True)

	## The constructor
	def __init__(self, title=None, message=None, show_on_date=None):
		self.title = title
		self.message = message
		self.show_on_date = show_on_date

# Price-table
# 
# Contains all the prices that are used
class Price(Base):
	__tablename__ = 'price'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True, unique=True)
	information = db.Column(db.UnicodeText())
	price = db.Column(db.Integer)

	## The constructor
	def __init__(self):
		return

## Quote-table
#
# Contains the quotes added
class Quote(Base):
	__tablename__ = 'quote'
	id = db.Column(db.Integer(), primary_key=True)
	quote = db.Column(db.String(254), index=True)

	## The constructor
	def __init__(self, quote):
		self.quote = quote

## Register code-table
#
# Contains the 'unique' code that are used on registration
class RegisterCode(Base):
	__tablename__ = 'register_code'
	id = db.Column(db.Integer(), primary_key=True)
	code = db.Column(db.String(10), index=True, unique=True)

	## The constructor
	def __init__(self, code=None):
		self.code = code

## Schedule date-table
# 
# Contains which weekday and what date a scheduled event is on
class Schedule(Base):
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

	# Two different for two paragraphs
	activity_info_day = db.Column(db.UnicodeText())
	activity_info_evening = db.Column(db.UnicodeText())

	## The constructor
	def __init__(self, week=None, date=None, weekday=None, href_div_id=None,
				 img_url=None, time=None, place=None, activity_info_day=None, activity_info_evening=None):
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

## School classes-table
#
# Contains the different school classes
class SchoolClass(Base):
	__tablename__ = 'school_class'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(100), index=True, unique=True)
	schedule = db.Column(db.String(254), index=True)
	fk_school_program_id = db.Column(db.Integer(), db.ForeignKey('school_program.id'))

	## The constructor
	def __init__(self, name=None, schedule=None, fk_school_program_id=None):
		self.name = name
		self.schedule = schedule
		self.fk_school_program_id = fk_school_program_id

## School classes-table
# 
# Contains the school classes that the student can choose between when register
class SchoolProgram(Base):
	__tablename__ = 'school_program'
	id = db.Column(db.Integer(), primary_key=True)
	abbreviation = db.Column(db.String(5), index=True, unique=True)
	name = db.Column(db.String(100), index=True, unique=True)
	r_school_class = db.relationship('SchoolClass', backref='SchoolProgram')

	## The constructor
	def __init__(self, id=None, abbreviation=None, name=None):
		self.id = id
		self.abbreviation = abbreviation
		self.name = name

## Student poll answers-table
# 
# Contains all the students' answers for the student poll
class StudentPollAnswer(Base):
	__tablename__ = 'student_poll_answer'
	id = db.Column(db.Integer, primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	fk_student_poll_question_id = db.Column(db.Integer, db.ForeignKey('student_poll_question.id'))

	## Will return the question id as an int instead of a StudentPollAnswer object.
	## Need this to check the MultiDict in profile_student_poll
	def __int__(self):
		return self.fk_student_poll_question_id

	## The constructor
	def __init__(self, fk_user_id=None, fk_student_poll_question_id=None):
		self.fk_user_id = fk_user_id
		self.fk_student_poll_question_id = fk_student_poll_question_id
		return

## Student poll assigned group-table
# 
# Contains which group the student is assigned to
class StudentPollAssignedGroup(Base):
	__tablename__ = 'student_poll_assigned_group'
	id = db.Column(db.Integer(), primary_key=True)
	fk_student_poll_dialect_id = db.Column(db.Integer, db.ForeignKey('student_poll_dialect.id'))
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	position = db.Column(db.Integer())

	## The constructor
	def __init__(self, fk_student_poll_dialect_id=None, fk_user_id=None, position=None):
		self.fk_student_poll_dialect_id = fk_student_poll_dialect_id
		self.fk_user_id = fk_user_id
		self.position = position

## Student poll dialect-table
# 
# Contains the dialects for the student poll
class StudentPollDialect(Base):
	__tablename__ = 'student_poll_dialect'
	id = db.Column(db.Integer, primary_key=True)
	dialect = db.Column(db.String(100), index=True, unique=True)
	max_students = db.Column(db.Integer(), default=0)
	r_student_poll_point = db.relationship('StudentPollPoint', backref='StudentPollDialect')
	r_student_poll_assigned_group = db.relationship('StudentPollAssignedGroup', backref='StudentPollDialect')

	## The constructor
	def __init__(self, id=None, dialect=None, max_students=None):
		self.id = id
		self.dialect = dialect
		self.max_students = max_students
		return

## Student poll point-table
# 
# Contains what point each student had for a specific student poll question
class StudentPollPoint(Base):
	__tablename__ = 'student_poll_point'
	id = db.Column(db.Integer, primary_key=True)
	fk_student_poll_dialect_id = db.Column(db.Integer, db.ForeignKey('student_poll_dialect.id'))
	fk_student_poll_question_id = db.Column(db.Integer, db.ForeignKey('student_poll_question.id'))
	point = db.Column(db.Integer)

	## The constructor
	def __init__(self, fk_student_poll_dialect_id=None, fk_student_poll_question_id=None, point=None):
		self.fk_student_poll_dialect_id = fk_student_poll_dialect_id
		self.fk_student_poll_question_id = fk_student_poll_question_id
		self.point = point
		return

## Student poll prefix-table
# 
# Contains the prefixes f or the student poll
class StudentPollPrefix(Base):
	__tablename__ = 'student_poll_prefix'
	id = db.Column(db.Integer, primary_key=True)
	prefix = db.Column(db.String(100), index=True, unique=True)
	r_question = db.relationship('StudentPollQuestion', backref='StudentPollPrefix', lazy='joined')

	## The constructor
	def __init__(self, id=None, prefix=None):
		self.id = id
		self.prefix = prefix
		return

## Student poll questions-table
# 
# Contains all the questions for the student poll
class StudentPollQuestion(Base):
	__tablename__ = 'student_poll_question'
	id = db.Column(db.Integer, primary_key=True)
	fk_student_poll_prefix_id = db.Column(db.Integer, db.ForeignKey('student_poll_prefix.id'))
	question = db.Column(db.String(100), index=True)
	r_question_point = db.relationship('StudentPollPoint', backref='StudentPollQuestion', lazy='joined')

	## The constructor
	def __init__(self, student_poll_prefix_id=None, question=None):
		self.fk_student_poll_prefix_id = student_poll_prefix_id
		self.question = question
		return

## User-table
# 
# Contains all the registered users
class User(Base):
	__tablename__ = 'user'
	id = db.Column(db.Integer(), primary_key=True)
	email = db.Column(db.String(100), index=True, unique=True)
	password = db.Column(db.String(254), index=True)
	role = db.Column(db.SmallInteger(), default=ROLE_USER)
	r_user_information = db.relationship('UserInformation', backref='user', lazy='joined', uselist=False)
	r_student_poll = db.relationship('StudentPollAnswer', backref='user', lazy='dynamic')
	r_student_poll_assigned_group = db.relationship('StudentPollAssignedGroup', backref='user')
	r_gallery_album = db.relationship('GalleryAlbum', backref='user')
	r_gallery_picture = db.relationship('GalleryPicture', backref='user')

	## The constructor
	def __init__(self, email=None, password=None, role=ROLE_USER):
		self.email = email
		self.password = password
		self.role = role

## User information-table
# 
# Contains a user's information. Connected with User with fk_user_id
# ATTENTION: school_program and school_class should be foreign keys!
class UserInformation(Base):	
	__tablename__ = 'user_information'
	id = db.Column(db.Integer(), primary_key=True)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	firstname = db.Column(db.String(100), index=True, default='')
	lastname = db.Column(db.String(100), index=True, default='')
	allergies = db.Column(db.String(254), index=True, default='')
	food_preference = db.Column(db.SmallInteger(), index=True, default=0)
	phonenumber = db.Column(db.String(15), index=True, default='')
	phonenumber_vis = db.Column(db.SmallInteger, index=True, default=0)
	facebook_url = db.Column(db.String(100), index=True, default='')
	school_program = db.Column(db.SmallInteger(), index=True, default=0)
	school_class = db.Column(db.SmallInteger(), index=True, default=0)
	current_city = db.Column(db.String(100), index=True, default='')
	where_from = db.Column(db.String(100), index=True, default='')
	presentation = db.Column(db.UnicodeText())
	login_count = db.Column(db.Integer(), default=0)
	poll_done = db.Column(db.SmallInteger(), default=0)
	finished_profile = db.Column(db.SmallInteger(), default=0)
	recover_code = db.Column(db.String(50))
	bicycle = db.Column(db.SmallInteger(), default=0)
	fk_student_dialect = db.Column(db.Integer, db.ForeignKey('student_poll_dialect.id'))

	## The constructor
	def __init__(self, user_id=None, presentation=None):
		self.fk_user_id = user_id
		self.presentation = presentation