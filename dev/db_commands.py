#!/usr/bin/python
# -*- coding: utf-8 -*-

# READ
# http://www.blog.pythonlibrary.org/2010/02/03/another-step-by-step-sqlalchemy-tutorial-part-2-of-2/

import models
import config
import math
import read_csv
import read_quotes
import debug

# To get namedtuple
import collections

db = config.db
app = config.app
db_session = config.db_session

debug = debug.debug

school_program = []
school_program.append(models.SchoolProgram(1, 'D', 'Datateknik'))
school_program.append(models.SchoolProgram(2, 'IT', 'Informationsteknologi'))
school_program.append(models.SchoolProgram(3, 'IP', 'Innovativ Programmering'))
school_program.append(models.SchoolProgram(4, 'U', 'Mjukvaruteknik'))

school_class = []
school_class.append(models.SchoolClass(name='D0a', fk_school_program_id='1'))
school_class.append(models.SchoolClass(name='D0b', fk_school_program_id='1'))
school_class.append(models.SchoolClass(name='D0c', fk_school_program_id='1'))
school_class.append(models.SchoolClass(name='IT0', fk_school_program_id='2'))
school_class.append(models.SchoolClass(name='IP0', fk_school_program_id='3'))
school_class.append(models.SchoolClass(name='U0', fk_school_program_id='4'))

contacts = []
contacts.append(models.Contact('Patrik Hillgren', '070-0434527', 'pathi747@student.liu.se', 0, 'IT0',''))
contacts.append(models.Contact('Alicia Tonolli', '070-4237004', 'alito938@student.liu.se', 0, 'D0a',''))
contacts.append(models.Contact('Johan Falk', '070-8468608', 'johfa808@student.liu.se', 0, 'D0b',''))
contacts.append(models.Contact('Tony Fredriksson', '070-6745520', 'tonfr314@student.liu.se', 0, 'D0c',''))
contacts.append(models.Contact('Gustav Bylund', '073-0262686', 'gusby403@student.liu.se', 0, 'IP0',''))
contacts.append(models.Contact('Alex Telon', '070-2647531', 'alete471@student.liu.se', 0, 'U0',''))
contacts.append(models.Contact('Siv Söderlund', '013-282836', 'siv.soderlund@liu.se', 1, '', 'http://www.liu.se/personal/tfk/sivso41?l=sv'))

if config.host_option.dev:
	# Should check if the DB is created successfully or not!
	def create_db():
		config.Base.metadata.create_all(bind=config.engine, checkfirst=True)
		return "DB creation done"

	def delete_db():
		config.Base.metadata.drop_all(bind=config.engine)
		return "JAAAA"

	def create_secret_code():
		db_session.add(models.RegisterCode('two_weevil'))
		db_session.commit()
		return 'Secret code added'
		# Add the secret code to the DB!
		# two_weevil

	def create_school_classes():
		for classes in school_class:
			db_session.add(classes)
		db_session.commit()
		return "School classes added"

	def create_school_programs():
		for program in school_program:
			db_session.add(program)
		db_session.commit()
		return "School programs added"

	def create_contacts():
		for contact in contacts:
			db_session.add(contact)
		db_session.commit()
		return "Contacts added"

	def create_student_poll():
		# '/www/dstaben/htdocs/dev/studentpoll.csv'
		# os.getcwd() + '/dev/studentpoll.csv'
		StudentPoll = read_csv.ReadStudentPollCsvFile(config.host_option.student_poll_file)

		# Add prefixes
		for index, p in StudentPoll.get_prefixes().iteritems():
			db_session.add(models.StudentPollPrefix(index, p))

		# Add questions
		for index, dict_content in StudentPoll.get_questions().iteritems():
			for q in dict_content:
				db_session.add(models.StudentPollQuestion(index, q))

		# Add dialects
		max_students = StudentPoll.get_max_students()
		for index, d in StudentPoll.get_dialects().iteritems():
			db_session.add(models.StudentPollDialect(index, d, max_students[index]))

		# Add points
		# Get the points from the CSV file
		for index_in_db, points_dict in StudentPoll.get_points().iteritems():
			# Get the question and 
			for question, point_list in points_dict.iteritems():
				for dialect_index, point in enumerate(point_list):
					if point != '':
						dialect_id = dialect_index+1
						question_id = index_in_db
						db_session.add(models.StudentPollPoint(dialect_id, question_id, point))
		db_session.commit()
		return 'Student poll prefixes and questions added'

	def create_quotes():
		try:
			Quotes = read_quotes.ReadQuotes(config.host_option.quote_file)

			# Add quotes
			for quote in Quotes.get_quotes():
				db_session.add(models.Quote(quote))

			db_session.commit()
			return 'Quotes added'
		except:
			return 'Could not add quotes'

def add_contact(name, phonenumber, email, role, school_class, link):
	contact = models.Contact(name, phonenumber, email, role, school_class, link)
	db_session.add(contact)
	db_session.commit()
	return 'success'

def add_login_count(db_user_email):
	db_user = models.User.query.filter_by(email=db_user_email).first()
	user_info = models.UserInformation.query.filter_by(fk_user_id=db_user.id).first()
	user_info.login_count += 1
	db_session.commit()

def add_user_information(db_user_id):
	try:
		db_session.add(models.UserInformation(db_user_id, ''))
		db_session.commit()
		return True
	except:
		return False

def check_role(db_user_email):
	return models.User.query.filter_by(email=db_user_email).first().role

def check_if_email_exist(email):
	if models.User.query.filter_by(email=email).first():
		return True
	else:
		return False

def get_all_albums(approved):
	return models.GalleryAlbum.query.filter_by(approved=approved).all()

def get_a_album(album_id):
	return models.GalleryAlbum.query.filter_by(id=album_id).first()

def get_all_pic_from_album(album_id):
	return models.GalleryPicture.query.filter_by(fk_gallery_album_id=album_id).all()

def get_thumbnail(album_id):
	return models.GalleryPicture.query.filter_by(fk_gallery_album_id=album_id).first()

def save_album(uploader, date, time, title, description, approved):
	try:
		# return 'S'
		user_id = models.User.query.filter_by(email=uploader).first().id
		# return 'U'
		album = models.GalleryAlbum(user_id, date, time, title, description, approved)
		# return 'P'
		db_session.add(album)
		# return 'A'
		db_session.commit()
		# return '!'
		return models.GalleryAlbum.query.filter_by(fk_user_id=user_id, date=date, time=time, title=title).first().id
	except:
		return 'KUNDE EJ SPARA ALBUMET!'

def save_picture(uploader, album_id, date, time, path, description):
	try:
		user_id = models.User.query.filter_by(email=uploader).first().id
		picture = models.GalleryPicture(user_id, album_id, date, time, path, description)
		db_session.add(picture)
		db_session.commit()
		return models.GalleryPicture.query.filter_by(fk_user_id=user_id, fk_gallery_album_id=album_id, date=date, time=time, path=path).first().id
	except:
		return 'KUNDE EJ SPARA BILDEN!'

def update_picture(pic_id, description):
	models.GalleryPicture.query.filter_by(id=pic_id).update({"description": description})
	db_session.commit()

def album_approve(album_id):
	models.GalleryAlbum.query.filter_by(id=album_id).update({"approved": 1})
	db_session.commit()

def delete_album(album_id):
	album = models.GalleryAlbum.query.filter_by(id=album_id).first()
	db_session.delete(album)
	db_session.commit()
	return True

def get_user_name(user_id):
	first_name = models.UserInformation.query.filter_by(fk_user_id=user_id).first().firstname
	last_name = models.UserInformation.query.filter_by(fk_user_id=user_id).first().lastname
	name = first_name + ' ' + last_name
	return name

def get_class_mates(db_user_email):
	db_user = models.User.query.filter_by(email=db_user_email).first()
	if db_user.r_user_information.school_program > 0:
		return models.User.query.join(models.UserInformation).filter(models.User.role != 0, \
			models.UserInformation.school_program == db_user.r_user_information.school_program).all()
	else:
		return False

def get_comments(blog_id):
	return

def get_contacts(role):
	if role is 0:
		contacts = models.Contact.query.filter_by(role=role).order_by(models.Contact.school_class).all()
	else:
		contacts = models.Contact.query.filter_by(role=role).all()
	return contacts

def get_db_user(user_id=None, db_user_email=None, db_user_password=None, recover_code=None):
	# models.User.query.filter_by(id=1).first().user_information.fk_user_id
	if db_user_email != None:
		db_user = models.User.query.filter_by(email=db_user_email).first()
	elif user_id != None:
		db_user = models.User.query.filter_by(id=user_id).first()
	elif recover_code != None:
		# return db_session.query(models.User, models.UserInformation).join('user_information').filter_by(recover_code=recover_code).first()
		# return models.User.query.join(models.User.user_information).filter_by(recover_code=recover_code).first()
		return models.User.query.join(models.UserInformation).filter(models.UserInformation.recover_code==recover_code).first()

	if db_user is not None:
		db_user_info = {'user': db_user, 'info': models.UserInformation.query.filter_by(fk_user_id=db_user.id).first()}

		# Check to see if a user is signing in
		if db_user_password is not None:
			if config.bcrypt.check_password_hash(db_user.password, db_user_password):
				return db_user_info
			else:
				return False
		else:
			return db_user_info
	else:
		return False
		
def get_quotes():
	try:
		return models.Quote.query.all()
	except:
		return False

def get_recover_user(db_user_recover_code):
	return models.UserInformation.query.filter_by(recover_code=db_user_recover_code).first()

def get_register_code():
	return models.RegisterCode.query.first()

def get_schedule(week):
	return models.Schedule.query.filter_by(week=week).order_by(config.asc(models.Schedule.id)).all()

def get_school_programs(program_abbreviation=None):
	if program_abbreviation:
		return models.SchoolProgram.query.filter_by(abbreviation=program_abbreviation).first()
	return models.SchoolProgram.query.all()

def get_school_classes():
	return models.SchoolClass.query.all()

def get_student_poll_answers(db_user_email):
	user_id = get_db_user(db_user_email=db_user_email)['user'].id
	return models.StudentPollAnswer.query.filter_by(fk_user_id=user_id).order_by(models.StudentPollAnswer.id).all()

def get_student_poll_dialects():
	return models.StudentPollDialect.query.order_by(models.StudentPollDialect.id).all()

def get_student_poll_points():
	return models.StudentPollPoint.query.order_by(models.StudentPollPoint.fk_student_poll_question_id).all()

def get_student_poll_prefix():
	admin_prefix_id = models.StudentPollPrefix.query.filter_by(prefix = 'Admin').first().id
	return models.StudentPollPrefix.query.filter(models.StudentPollPrefix.id != admin_prefix_id).order_by(models.StudentPollPrefix.id).all()

def get_student_poll_question():
	admin_prefix_id = models.StudentPollPrefix.query.filter_by(prefix = 'Admin').first().id
	return models.StudentPollQuestion.query.filter(models.StudentPollQuestion.fk_student_poll_prefix_id != admin_prefix_id).order_by(models.StudentPollQuestion.id).all()

def get_user_school_program(db_user_email):
	db_user = models.User.query.filter_by(email=db_user_email).first()
	school_program = models.SchoolProgram.query.filter_by(id=db_user.r_user_information.school_program).first()
	if school_program != None:
		return school_program.abbreviation
	else:
		return 0

def get_school_program_users(school_program):
	if school_program == str(0):
		return models.User.query.join(models.UserInformation).filter(models.UserInformation.school_program==1).filter(models.User.role!=0).all()
	return models.User.query.join(models.UserInformation).filter(models.UserInformation.school_program==get_school_programs(school_program).id).filter(models.User.role!=0).all()

def register_user(db_user_dict):
	try:
		new_user = models.User(db_user_dict['email'], config.bcrypt.generate_password_hash(db_user_dict['password']))
		db_session.add(new_user)
		db_session.commit()
		return True
	except:
		return False

def save_student_poll(db_user_email, db_student_poll_dict):
	try:
		db_user = models.User.query.filter_by(email=db_user_email).first()
		for x in db_student_poll_dict:
			db_session.add(models.StudentPollAnswer(db_user.id, x))
		db_session.commit()
		return True
	except:
		return False

def add_blog_comment(request_form):
	try:
		new_comment = models.BlogComment(request_form['fk_user_id'], request_form['fk_blog_id'], request_form['comment'], request_form['date'], request_form['time'])
		# new_comment = models.BlogComment(1, 1, 'SAdds', '2013-08-27', '13:37:00')
		db_session.add(new_comment)
		db_session.commit()
		return True
	except:
		return False

def save_blog(blog_dict, blog_id=False):
	try:
		if not blog_id:
			db_session.add(models.Blog(blog_dict['fk_user_id'], blog_dict['fk_gallery_album_id'], blog_dict['title'], blog_dict['text'], blog_dict['date'], blog_dict['time']))
		elif blog_id:
			models.Blog.query.filter_by(id=blog_id).update(blog_dict)
		db_session.commit()
		return True
	except:
		return False

def get_blog(b_id=None, b_date=None):
	try:
		if b_id:
			return models.Blog.query.filter_by(id=b_id).all()
		elif b_date:
			return models.Blog.query.filter_by(date=b_date).first()
		else:
			return models.Blog.query.order_by(config.desc(models.Blog.id)).all()
	except:
		return False

def check_if_blog_done(date):
	return models.Blog.query.filter_by(date=date).first()

def get_gallery(g_id=None):
	try:
		if not g_id:
			return models.GalleryAlbum.query.all()
		else:
			return models.GalleryAlbum.query.filter_by(id=g_id)
	except:
		return False

def update_db_user(db_user_email, db_user_dict):
	try:
		db_user = models.User.query.filter_by(email=db_user_email).first()
		models.UserInformation.query.filter_by(fk_user_id=db_user.id).update(db_user_dict)
		# models.User.query.join(models.User.user_information).filter_by(recover_code=recover_code).first()
		# models.User.query.join(models.User.user_information).filter_by(id=db_user.id).update({'recover_code': 'fff', 'firstname': 'asd'})
		db_session.commit()
		return True
	except:
		return False

def update_db_pw(db_user_email, db_user_dict):
	db_user = models.User.query.filter_by(email=db_user_email).first()
	if db_user_dict['new_password'] == db_user_dict['repeat_password'] and \
	config.bcrypt.check_password_hash(db_user.password, db_user_dict['current_password']):
		models.User.query.filter_by(email=db_user_email).update({'password': config.bcrypt.generate_password_hash(db_user_dict['new_password'])})
		db_session.commit()
		return True
	else:
		return False

def update_db_pw_from_code(db_user_email, db_user_dict):
	try:
		db_user = models.User.query.filter_by(email=db_user_email).first()
		models.User.query.filter_by(email=db_user_email).update({'password': config.bcrypt.generate_password_hash(db_user_dict['new_password'])})
		db_session.commit()
		return True
	except:
		return False	


##############
# ADMIN TOOLS #
##############
def add_student_poll_prefix(db_student_poll_dict):
	try:
		new_prefix = models.StudentPollPrefix(db_student_poll_dict['prefix'])
		db_session.add(new_prefix)
		db_session.commit()
		return True
	except:
		return False

def add_student_poll_question(db_student_poll_dict):
	try:
		new_question = models.StudentPollQuestion(db_student_poll_dict['prefix'], db_student_poll_dict['question'])
		db_session.add(new_question)
		db_session.commit()
		return True
	except:
		return False

def add_student_poll_max_students(db_student_poll_dict):
	try:
		models.StudentPollDialect.query.filter_by(id=db_student_poll_dict['id']).update({'max_students':db_student_poll_dict['max_students']})
		db_session.commit()
		return True
	except:
		return False

def admin_add_quote(form_value):
	try:
		# !!!!!!
		# Need to check for STABEN fonts and shiiiiet
		new_quote = models.Quote(form_value['quote'])
		db_session.add(new_quote)
		db_session.commit()
		return True
	except:
		return False

def admin_get_all_student_poll_answers():
	# asd = models.StudentPollAnswer.query.order_by(models.StudentPollAnswer.fk_user_id).all()
	# db_user_info = {'user': db_user, 'info': models.UserInformation.query.filter_by(fk_user_id=db_user.id).first()}
	return models.StudentPollAnswer.query.order_by(models.StudentPollAnswer.fk_user_id).all()

def admin_calc_user_points(user_id, order=False, nr_of_points=None):
	points = models.StudentPollPoint.query.all()
	questions_w_points = models.StudentPollQuestion.query.order_by(models.StudentPollQuestion.id).all()

	# {Question_id: {Dialect_id: Point}}
	# MultiDict([(QuestionID, MultiDict([(Dialect_id: Point), (Dialect_id: Point)]))])
	questions_w_dialects_a_points = config.MultiDict()
	for question in questions_w_points:
		point_MD = config.MultiDict()
		for point in question.r_question_point:
			point_MD.add(point.fk_student_poll_dialect_id, point.point)
		questions_w_dialects_a_points.add(question.id, point_MD)

	# MultiDict([(Dialect_id, Point), (Dialect_id, Point)])
	# The answers from user_id
	# Add all the dialects with the points
	# 100 IS ADDED AS A DIALECT
	# NOOOOOO IDEA WHYYYYYY =(
	answers = models.StudentPollAnswer.query.filter_by(fk_user_id=user_id).all()
	dialects_w_points = config.MultiDict()
	for answer in answers:
		for dialect_id, point in questions_w_dialects_a_points[answer.fk_student_poll_question_id].iteritems():
			if dialect_id != 100:
				dialects_w_points.add(dialect_id, point)

	# MultiDict([(Missing_dialect_id, 0), (Missing_dialect_id, 0)])
	# Add the missing dialect id(s) with zero points to dialects_w_points
	for i in range(1, len(get_student_poll_dialects())+1):
		if not dialects_w_points.get(i):
			dialects_w_points.add(i, 0)

	# Get the total points for all dialects
	# If the dialect ID exist in dialect_w_total_points_md it will add the \
	# points to that dialect
	# Else it will add that dialect with the initial point
	dialect_w_total_points_md = config.MultiDict()
	for key, value in dialects_w_points.iteritems(multi=True):
		if dialect_w_total_points_md.has_key(key):
			dialect_w_total_points_md[key] = dialect_w_total_points_md[key]+value
		else:
			dialect_w_total_points_md.add(key, value)

	# If order is True then it will return a dict with the highest student group at first place
	if order is True:
		# print dialect_w_total_points_md
		# print dialect_w_total_points_md.to_dict()
		dialect_w_total_points_md = sort_dict(dialect_w_total_points_md.to_dict())

	return dialect_w_total_points_md

def admin_get_user_poll_answer(user_id):
	userinfo_w_answers = models.User.query.filter_by(id=user_id).join(models.User.r_user_information).join(models.User.r_student_poll).all()
	prefixes_w_questions_w_points = models.StudentPollPrefix.query.order_by(models.StudentPollPrefix.id).all()

	pref_w_ques_w_point_OMD = config.OrderedMultiDict()
	for content in prefixes_w_questions_w_points:
		questions_OMD = config.OrderedMultiDict()
		for question in content.r_question:
			dialect_id_w_points_OMD = config.OrderedMultiDict()
			for point in question.r_question_point:
				dialect_id_w_points_OMD.add(point.fk_student_poll_dialect_id, point.point)
			inner_OMD = config.OrderedMultiDict()
			inner_OMD.add('question', question.question)
			inner_OMD.add('points', dialect_id_w_points_OMD)
			questions_OMD.add(question.id, inner_OMD)
		pref_w_ques_w_point_OMD.add(content.prefix, questions_OMD)
	
	userinfo_w_answers_MD = config.MultiDict()
	for userinfo in userinfo_w_answers:
		userinfo_w_answers_MD.add('userinfo', userinfo.r_user_information)
		for answer in userinfo.r_student_poll:
			userinfo_w_answers_MD.add(answer.fk_student_poll_question_id, answer.fk_student_poll_question_id)
	#, 4: admin_calc_user_points(user_id)
	return {1: userinfo_w_answers_MD, 2: pref_w_ques_w_point_OMD}

def admin_get_all_users():
	return models.User.query.all()

def admin_get_all_users_w_poll_done():
	return models.UserInformation.query.filter_by(poll_done=1)

def dialect_full(md, dialect_id, max_students):
	return max_students <= len(md.getlist(dialect_id))

def check_if_user_in_md(md, user_id):
	return

def check_points(md, r_md, d_id, u_id, u_point):
	# OBS!
	# I am assume that the u_id has the same point on d_id

	# md = MultiDict([DialectID, {UserID: TotalPoints}])
	poped_list = md.poplist(d_id)
	lowest_point = 100

	# Loop the poped list
	# Loop through the dict which is in content
	for i, content in enumerate(poped_list):
		for user_id, user_point in content.iteritems():
			# If u_point is higher than user_point
			#  and
			#  if lowest_point is lower than user_point
			#  it will set the new lowest point
			if u_point > user_point and lowest_point > user_point:
				lowest_point = user_point
				lowest_point_index = i
				# print u_id, '-', u_point, '----', user_id, '-', user_point

	# If there is not a lower point in the dialect_id it will only return
	#  the md as is
	# If lowest_point is not 100 (default value) it will
	#  add the poped_list to r_md
	#  and
	#  replace that spot in poped_list with the new user with point
	if lowest_point != 100:
		r_md.add(d_id, poped_list[lowest_point_index])
		poped_list[lowest_point_index] = {u_id: u_point}

	# Add everything back to the md
	for item in poped_list:
		md.add(d_id, item)

# def check_and_replace_user_in_md(md, r_md, d_id, u_id, u_point):
# 	# md = MultiDict([DialectID, {UserID: TotalPoints}])
# 	# print {u_id: u_point} in md.getlist(d_id)
# 	# print 'user id', u_id
# 	# print md.getlist(d_id)
# 	# print ''
# 	print md
# 	for dialect_id, content in md.iteritems():
# 		print 'UID:', u_id
# 		print 'DID:', dialect_id, '- Content:', md.getlist(dialect_id)
# 		for l in md.getlist(dialect_id):
# 			if l.get(u_id):
# 				print l
# 	# 	for x in content.iteritems():
# 	# 		print x
# 	# print ''
# 	# 	for a, b in content.iteritems():
# 	# 		print a, b
# 	# print ''
# 		# replace_value = {u_id: u_point}
# 		# if replace_value in md.getlist(dialect_id):
# 		# 	print md.getlist(dialect_id)
# 		# 	print replace_value

# WORK (19-08)
def add_to_groups(md):
	# md = MultiDict(DialectID, MultiDict(UserID, Point))
	# {UserID: UserIDPoint, UserID: UserIDPoint}
	# print md
	groups = config.MultiDict()
	for dialect_id, content in md.iterlists():
		# print dialect_id
		# print content
		asd = config.MultiDict()
		for index, user_md in enumerate(content):
			# print user_md.keys()[0]
			# print user_md.values()[0]
			# print '###'
			if user_md.values()[0] > 10:
				asd.add(user_md.keys()[0], user_md.values()[0])
		# print '$$$$$$'
		groups.add(dialect_id, asd)
	# 	user_w_point = config.MultiDict()
	# 	for dialect_id, user_id_point in content.iteritems():
	# 		user_w_point.add(user_id, user_id_point)
	# 	groups.add(dialect_id, user_w_point)
	# Will return: MultiDict(DialectID, MultiDict([(UserID, UserIDPoint), (UserID, UserIDPoint)]))
	return groups

# WORK (19-08)
def sort_groups(md):
	# md = MultiDict(DialectID, MultiDict([(UserID, UserIDPoint), (UserID, UserIDPoint)]))
	dsa = config.OrderedMultiDict()
	# content is a list with MultiDicts in it
	for dialect_id, content in md.iteritems():
		etst = {}
		# print 'DialectID:', dialect_id
		# print 'Content:', content
		# lowest_score = 100
		for user_id, user_id_point in content.iteritems():
			etst[user_id] = user_id_point
			# user_id_point = content[index].values()[0]
			# if user_id_point < lowest_score:
			# 	# print user_id_point, 'lower than', lowest_score
			# 	# print ''
			# 	lowest_score = user_id_point
			# etst[content[index].keys()[0]] = content[index].values()[0]
		etst = sort_dict(etst)
		dsa.add(dialect_id, etst)
		# for user_id, user_id_point in etst.iteritems():
		# 	md.add(dialect_id, config.MultiDict(user_id, user_id_point))
		# print ''
	# print dsa
	return dsa

def check_for_duplication_user(md, u_id, u_id_point):
	return

def check_for_duplication(md, r_md):
	# print md
	# print ''
	# for dialect_id, content in md.iterlists():
	# 	print 'DialectID:', dialect_id
	# 	print 'Content:', content
	# 	for index, u_md in enumerate(content):
	# 		# keys() = userid
	# 		# values() = userpoint
	# 		check_for_duplication_user(md, u_md.keys()[0], u_md.values()[0])

	# 	print ''

	# ----> print md[2]

	# for content in md.values():
	# 	for user_id, user_id_point in content.iteritems():
			
	# Find the user_id that is currently active
	# Find that user in rest_md (if it occurs)
	# If the user's point in md is higher than every other occurencies
	#  in rest_md nothing happens
	# Else if the user's point is lower in md than the point in rest_md
	#  the user will be removed from md 

	# BUT I SHOULD ONLY CHECK IN MD IF A USER HAS MORE THAN ONE
	# OCCURENCIE
	# IF A USER HAS IT THE LOWEST POINT WILL BE REMOVE
	# ELSE NOTHING HAPPENS
	# AFTER THIS IS DONE IT SHOULD BE A CHECK SO THAT EACH GROUP HAS
	# IT'S MAXIMUM NUMBER OF STUDENTS, IF NOT JUST TAKE FROM REST_MD

	# ^^^^^^^^^^^^
	# 1. Loop through md to get dialect_id and content (which is a OrderedMultiDict(UserID, UserIDPoint))
	# 2. Loop through content to get UserID and UserIDPoint
	# 3. Loop through md again IF the dialectID is NOT the same as the one user_id is in
	# 4. Loop through c to get all UserIDs and UserIDPoints from md AGAIN
	#      to check if UserID is in md more than once
	# 5. Check if the user exists more than once in md
	# 6. Check if the point in the second md is higher than in the
	#      first md
	# 7. Save this entry
	# 8. Remove the 'original' one with the lower score
	# 9. 
	return_values = collections.namedtuple('returns', ['md', 'rest_md'])

	asd = md
	for dialect_id, content in asd.iteritems(): #1
		# print 'DID:', dialect_id
		# print 'CONTENT:', content
		for user_id, user_id_point in content.iteritems(): #2
			# print 'Checking', user_id, 'with', user_id_point, 'points in DialectID', dialect_id
			for d_id, c in asd.iteritems(): #3
				if d_id != dialect_id: #3
					for u_id, u_id_point in c.iteritems(): #4
						if u_id is user_id: #5
							if u_id_point > user_id_point: #6
								# print 'Found a duplicated user higher points. UserID:', u_id, 'with', u_id_point, 'points in DialectID', d_id
								new_entry = (u_id, u_id_point) #7
								content.poplist(u_id) #8
	# Check in rest_md for u_id and remove all occurances!
	return return_values(md, remove_from_md(r_md, user_id))
				# for u_id, u_id_point in c.iteritems():

	# for dialect_id, content in md.iteritems():
	# 	print ''
	# 	print 'DID:', dialect_id
	# 	print 'MD:', content
	# 	print 'REST:', r_md
	# 	for user_id, user_id_point in content.iteritems():
	# 		for rest_u_id, rest_u_id_point in r_md.values()[0].iteritems():
	# 			if user_id == rest_u_id:
	# 				print user_id, user_id_point
	# 				print rest_u_id, rest_u_id_point
	# 				print '####'
	# 		print ''
	# 	print ''

def remove_from_md(md, u_id):
	# SHOULD I CHECK POINTS AS WELL IF U_ID HAVE A HIGHER POINT IN REST_MD THAN
	#   IN THE GROUP THE USER IS ASSIGNED?
	# print 'Check for:', u_id
	# print 'In:', md

	# Loop through md
	# Loop through the md's content
	# If argument u_id is user_id it will be poped
	for dialect_id, content in md.iteritems():
		# print 'DID:', dialect_id
		# print 'CONTENT:', content
		for user_id, user_id_point in content.iteritems():
			# print user_id, u_id
			if u_id is user_id:
				# print '!!!!!!!!!!!!!!!!!!!!!!!!!!11111111111111111111111111111111111111 Found!'
				# print user_id
				content.poplist(user_id)
		# print 'NEW CONTENT:', content
	return md

def limit_groups(md):
	# md = OrderedMultiDict(DialectID, OrderedMultiDict(UserID, UserIDPoint)
	student_poll_dialects = get_student_poll_dialects()
	return_values = collections.namedtuple('returns', ['md', 'rest_md'])

	return_md = config.OrderedMultiDict()
	for dialect_id, content in md.iteritems():
		print ''
		print 'DID:', dialect_id
		print 'MD:', content
		print 'REST:', r_md
		for user_id, user_id_point in content.iteritems():
			for rest_u_id, rest_u_id_point in r_md.values()[0].iteritems():
				if user_id == rest_u_id:
					print user_id, user_id_point
					print rest_u_id, rest_u_id_point
					print '####'
			print ''
		print ''


def limit_groups(md):
	# md = OrderedMultiDict(DialectID, OrderedMultiDict(UserID, UserIDPoint)
	student_poll_dialects = get_student_poll_dialects()
	return_md = config.OrderedMultiDict()
	return_values = collections.namedtuple('returns', ['md', 'rest_md'])

	rest_md = config.OrderedMultiDict()
	for dialect_id, content in md.iteritems():
		i = 1
		# print dialect_id
		user_w_point = config.OrderedMultiDict()
		user_w_point_rest = config.MultiDict()
		for user_id, user_id_point in content.iteritems():
			if i <= student_poll_dialects[dialect_id-1].max_students:
				# print user_id, user_id_point
				user_w_point.add(user_id, user_id_point)
			else:
				user_w_point_rest.add(user_id, user_id_point)
			i += 1
		return_md.add(dialect_id, user_w_point)
		rest_md.add(dialect_id, user_w_point_rest)
		# print ''

	return return_values(return_md, rest_md)

# WORK (19-08)
def prioritize_groups(md):
	group_dict = {}
	for dialect_id, content in md.iteritems():
		content_list = []
		for i in content:
			content_list.append(i)
		group_dict[dialect_id] = len(content_list)

	# Will return: OrderedMultiDict(DialectID, NumberOfStudents)
	return sort_dict(group_dict, True)

# WORK (19-08)
def populate_group_according_to_prio(md, priority_md):
	# Loop through md with the least prioritized group first
	# Save all userID's in a list
	# When looping through all the other groups in prioritized order,
	#   if the userID is in the list it will be removed from that group
	used_users = []

	# Need to check if a dialect is full when going in a prioritized order
	# If it is full then ignore all other users in that dialect and assign them
	# to other groups
	# ^^^^^^^^^^^^^^^
	
	# for i, x in md.iteritems():
	# 	print 'DialectID', i
	# 	print 'Content', x

	for prio_dialect_id, prio in priority_md.iteritems():
		for user_id, user_id_point in md[prio_dialect_id].iteritems():
			if not user_id in used_users:
				used_users.append(user_id)
				# Loop through md except prio_dialect_id and remove all instances of user_id in md
				for dialect_id, content in md.iteritems():
					if dialect_id != prio_dialect_id:
						for u_id, u_id_point in content.iteritems():
							if u_id is user_id:
								# print 'Found a duplicated user.'
								# print 'The original user is in:', prio_dialect_id
								# print 'The new user is in:', dialect_id
								content.pop(u_id)
						# print ''
	# print '########'
	# print priority_md
	# print '$$$$$$$$'
	# for i, x in md.iteritems():
	# 	print 'DialectID', i
	# 	print 'Content', x
	return md

def limit_group2(md):
	return_values = collections.namedtuple('returns', ['md', 'rest'])
	users_wo_group = []
	student_poll_dialects = get_student_poll_dialects()
	tree = config.OrderedMultiDict()
	for dialect_id, content in md.iteritems():
		adwq = config.OrderedMultiDict()
		i = 0
		for user_id, user_id_point in content.iteritems():
			if i < student_poll_dialects[dialect_id-1].max_students:
				adwq.add(user_id, user_id_point)
			else:
				users_wo_group.append(user_id)
			i += 1
		tree.add(dialect_id, adwq)

	# print len(users_wo_group)
	# print users_wo_group
	# for u_id in users_wo_group:
	# 	print u_id
	# 	print admin_calc_user_points(u_id)
	# return tree
	return return_values(tree, users_wo_group)

def assign_rest_users(md, rest_u, avail_groups):
	student_poll_dialects = get_student_poll_dialects()
	# print avail_groups
	# print rest_u
	used_users = []
	for u_id in rest_u:
		iiii = {}
		# print avail_groups
		# print admin_calc_user_points(u_id) = MultiDict(DialectID, Point)
		for dialect_id, point in admin_calc_user_points(u_id).iteritems():
			#point > 10 and 
			if dialect_id in avail_groups:
				iiii[point] = dialect_id
		iii = sort_dict(iiii)

		for point, dialect_id in iiii.iteritems():
			if not u_id in used_users and len(md[dialect_id]) < student_poll_dialects[dialect_id-1].max_students:
				used_users.append(u_id)
				md[dialect_id].add(u_id, point)
			# if not u_id in used_users and len(md[dialect_id]) < student_poll_dialects[dialect_id-1].max_students:
			# 	used_users.append(u_id)
			# 	md.add(dialect_id, config.MultiDict(u_id, point))

		# for i, x in priority_md.iteritems():
		# 	print i, x
				# print 'DID:', dialect_id
				# print 'POINT:', point
				# md.add(dialect_id, )
					# if not u_id in used_users:
					# 	used_users.append(u_id)
		# 		iiii[dialect_id] = point

		# print ''
		# iiii = sort_dict(iiii)
		# md[dialect_id].add(u_id, point)

	return md

def available_groups(md):
	student_poll_dialects = get_student_poll_dialects()
	avail_groups = []
	# print md
	for dialect_id in md:
	# 	print 'DID:', dialect_id
	# 	print 'MAX STUDENTS:', student_poll_dialects[dialect_id-1].max_students
	# 	print 'LENGTH:', len(md[dialect_id].values())
	# 	print ''
		if len(md[dialect_id].values()) < student_poll_dialects[dialect_id-1].max_students:
			avail_groups.append(dialect_id)
	return avail_groups

def admin_insert_user_to_group():
	# Going to try to send a finished md to a function and sort it from there
	# rest_md = config.MultiDict()

	# admin_get_top_groups_users_only returns: MultiDict(DialectID, MultiDict(UserID, Point))
	md = add_to_groups(admin_get_top_groups_users_only(10))
	# admin_get_top_groups_users_only(7)
	# for i, x in md.iteritems():
	# 	print i, ' --- ', x
	# print md
	# print '####'
	# print md
	md = sort_groups(md)
	# print md
	# print ''
	md = populate_group_according_to_prio(md, prioritize_groups(md))
	# print ''
	# limited = limit_group2(md)
	# md = limited.md
	# rest_users = limited.rest

	# # asd = available_groups(md)
	# # for i, x in md.iteritems():
	# # 	if i in asd:
	# # 		print i, ' --- ', x
	# # print ''
	# md = assign_rest_users(md, rest_users, available_groups(md))

	# users = []
	# for i, x in md.iteritems():
	# 	for user_id, point in x.iteritems():
	# 		users.append(user_id)
	# print len(users)
	# print sorted(users)

	print md

	# # Need to get all the users that got discarded = CHECK
	# # When all the discarded users are in rest_md = CHECK
	# # I need to to check for duplicated users = CHECK
	# # and if there is I just need to keep the highest point = CHECK
	# # in md = CHECK
	# # After that I need to populate all groups again so they are at it's maximum = NOPE!
	# #    THIS IS NOT NECESSARY SINCE ALL USER HAS A UNIQUE GROUP AND IN REST_MD THERE ARE ONLY DUPLICATED USERS
	# #    OR IS IT?
	# #    CASE 1: A USER GOT INTO GROUPS THAT HAS A LOT OF OTHER STUDENTS WITH HIGHER POINTS THAN THE STUDENT
	# #	 >> AFTER SOME 'RESEARCH' I HAVE FOUND THAT THIS IS NECESSARY

	# limited = limit_groups(md)
	# md = limited.md
	# rest_md = limited.rest_md # Should fix so that rest_md is sorted to!

	# print 'AFTER LIMIT_GROUPS'
	# print 'MD'
	# # print md
	# for i, x in md.iteritems():
	# 	print i, ' --- ', x
	# print '####'
	# print 'REST_MD'
	# print rest_md
	# print '@@@@'

	# duplications = check_for_duplication(md, rest_md)
	# md = duplications.md
	# rest_md = duplications.rest_md

	# print 'AFTER CHECK_FOR_DUPLICATION'
	# print 'MD'
	# # print md
	# for i, x in md.iteritems():
	# 	print i, ' --- ', x
	# print '$$$$'
	# print 'REST_MD'

def admin_insert_user_to_group():
	# Going to try to send a finished md to a function and sort it from there
	rest_md = config.MultiDict()
	md = add_to_groups(admin_get_top_groups_users_only(3))
	md = sort_groups(md)
	# Need to get all the users that got discarded = CHECK
	# When all the discarded users are in rest_md = CHECK
	# I need to to check for duplicated users
	# and if there is I just need to keep the highest point
	# in md
	
	limited = limit_groups(md)
	md = limited.md
	rest_md = limited.rest_md

	check_for_duplication(md, rest_md)

	# for i, x in md.iteritems():
	# 	print i, x
	# print rest_md



	# for i, x in md.iteritems():
	# 	print i, x
	# print '#####'
	# for o, c in rest_md.iteritems():
	# 	print o, c

	# Do this after I checked rest_md for duplications
	# populate_groups(md, rest_md) 

	# dialect_md = config.MultiDict()
	# rest_md = config.MultiDict()
	# student_poll_dialects = get_student_poll_dialects()

	# # admin_get_top_groups_users_only() returns OrderedMultiDict([(UserID, {DialectID, TotalPoints})])
	# for user_id, content in admin_get_top_groups_users_only(5).iteritems():
	# 	for dialect_id, total_point in content.iteritems():
	# 		# max_students = student_poll_dialects[dialect_id-1].max_students
	# 		dialect_md.add(dialect_id, {user_id: total_point})

	# 		# If the specific dialect_id does not have it's maximum number of students
	# 		#  it will add the user to it
	# 		# if not dialect_full(dialect_md, dialect_id, max_students):
	# 		# else:
	# 			# Replace current user with user_id if he has a higher score
	# 			#  than the current user in dialect_md[dialect_id]
	# 			# check_points(dialect_md, rest_md, dialect_id, user_id, total_point)
	# 			# check_and_replace_user_in_md(dialect_md, rest_md, dialect_id, user_id, total_point)



		### OLD!!!!!!!
		# for i, dialect_id in enumerate(content):
		# 	# Add 1 to i because i starts with 0
		# 	position = i+1

		# 	# Check so there is no more than max_students in a group.
		# 	# If there are more than student_poll_dialects[dialect_id].max_students
		# 	# students they will be added to rest_list to be dealt with later.
		# 	if len(dialect_md.getlist(dialect_id)) < student_poll_dialects[dialect_id-1].max_students:
		# 		dialect_md.add(dialect_id, {user_id: position})
		# 	# If user_id does not exist in dialect_md
		# 	elif not check_if_in_md(dialect_md, user_id):
		# 		# If True it will replace the values
		# 		# If False it will add the value to rest_md
		# 		# if check_if_in_md(dialect_md, user_id, position):
		# 			# print replace_position_in_md(dialect_md, dialect_id, , {user_id: position})

		# 		# If dialect_id is full in dialect_md,
		# 		# check if the current user_id has a higher position then
		# 		# any of the users already in dialect_md
		# 		#
		# 		# If true, the current user will swap with the user
		# 		# in dialect_md and that user will be added to rest_list
		# 		#
		# 		# If false, the current user will be added to rest_list

		# 		# PROBLEM
		# 		# This adds a user to rest_md EVEN if that user is in dialect_md
		# 		# but with two other positions.
		# 		# E.g.: If a user that has position 1 replaces user2 with position 2, then
		# 		# user2 will be added to rest_md even if user2's position 1 and 3 is in
		# 		# dialect_md
		# 		found = False
		# 		for list_position, ze_list in enumerate(dialect_md.getlist(dialect_id)):
		# 			for list_user_id, list_user_position in ze_list.iteritems():
		# 				if position < list_user_position:
		# 					# replace_position_in_md(dialect_md.getlist(dialect_id), list_user_position, position)
		# 					dialect_md = replace_position_in_md(dialect_md, dialect_id, list_position, \
		# 						{user_id: position})
		# 					print 'Replaced:', {user_id: position}, 'with:', {list_user_id: list_user_position}
		# 					user_id = list_user_id
		# 					found = True
		# 			if found: break #Ugly solution but it works...
		# 		rest_md.add(dialect_id, {user_id: list_user_position})
		# 	# If the user exist in dialect_md
		# 	else:
		# 		print '######', user_id
		

	# print ''
	# print 'DialectID: [{UserID: Position}]'
	# for a, d in dialect_md.iterlists():
	# 	print 'Dialect ID: ', a, ' has: ', d
	# print ''
	# print 'DialectID, {UserID: Position}'
	# for k, l in rest_md.iterlists():
	# 	print 'DialectID:', k, ' has: ', l

def admin_get_top_three_groups():
	###
	# Not sure that colors are needed!
	###
	top_three_groups = {}
	for i in admin_get_all_users_w_poll_done():
		# content will contain the information gathered
		content = {}

		# This is a really ugly way to do it, it should be a better way!
		# dialect_w_total_points = OrderedMultiDict([(DialectID, TotalPoints)])
		# dialect_w_total_points_colors = OrderedMultiDict([(DialectID, ColorCode)])
		# OrderedMultiDict([(DialectID, {'tot_points': points, 'color': ColorCode})])
		dialect_w_total_points = config.OrderedMultiDict()
		dialect_w_total_points_colors = config.OrderedMultiDict()

		# Loop the specific user's top three groups and add to the MultiDict
		for dialect_id, total_point in admin_calc_user_points(i.fk_user_id, True).iteritems():
			if len(dialect_w_total_points) < 3:
				dialect_w_total_points.add(dialect_id, total_point)

				# This is soooo ugly
				# Gotta find out another way to do this!
			
				if len(dialect_w_total_points) is 1:
					dialect_w_total_points_colors.add(dialect_id, '#00ff00')
				elif len(dialect_w_total_points) is 2:
					dialect_w_total_points_colors.add(dialect_id, '#ffff00')
				elif len(dialect_w_total_points) is 3:
					dialect_w_total_points_colors.add(dialect_id, '#ff0000')
			else:
				break

		content['top_score'] = dialect_w_total_points
		content['top_score_colors'] = dialect_w_total_points_colors
		content['user_points'] = admin_calc_user_points(i.fk_user_id)
		content['user'] = get_db_user(user_id=i.fk_user_id)['info']
		top_three_groups[i.fk_user_id] = content
	return top_three_groups

def admin_get_top_groups_users_only(number_of_groups=3):
	# top_three_groups = {}
	dsa = config.MultiDict()
	for i in admin_get_all_users_w_poll_done():
		# asd = config.MultiDict()
		# Loop the specific user's top groups and add to the MultiDict
		for dialect_id, total_point in admin_calc_user_points(i.fk_user_id, True).iteritems():
			# print dialect_id
			# print dialect_id, total_point
			# if len(asd) < number_of_groups:
			# asd.add(i.fk_user_id, total_point)
			# dsa.add(dialect_id, asd)
			dsa.add(dialect_id, config.MultiDict([(i.fk_user_id, total_point)]))

		# top_three_groups[dialect_id] = dialect_w_total_points
	# Will return: MultiDict(DialectID, MultiDict(UserID, Point))
	return dsa

def sort_dict(m_dict, desc=False):
	"""
	Add keys and values to a tuple that is within a list so it is possible to sort
	on the value (which is x[1] in sorted())
	"""
	tmp_list = [(key, value) for key, value in m_dict.iteritems()]
	tmp_list = sorted(tmp_list, key=lambda x: x[1])


	"""
	Loop the sorted values into an OrderedMultiDict().
	This is so the function return a MultiDict() and not a list with tuples
	"""
	if not desc:
		tmp_list.reverse()	
	new_omd = config.OrderedMultiDict()
	for a, b in tmp_list:
		new_omd.add(a, b)

	return new_omd

# def check_if_in_md(md, user_id, position=None):
# 	# DialectID: [{UserID: Position}, {UserID: Position}]
# 	# Loop through the MD
# 	# Loop through all dicts
# 	# If user_id is in c (which is a dict) it returns True
# 	# If position is set it will check if the user's position in the md is higher than the position set
# 	# E.g. {5: 3} is higher than {5: 2}
# 	for dialect_id, content in md.iterlists():
# 		for c in content:
# 			if user_id in c:
# 				if position != None:
# 					print 2222222
# 					print position, c
# 					if position < c.get(user_id):
# 						return c
# 					else:
# 						return False
# 				else:
# 					return True
# 	return False

def replace_position_in_md(md, dialect_id, list_position, new_value):
	poped_list = md.getlist(dialect_id)
	poped_list.pop(list_position)
	poped_list.append(new_value)

	md.poplist(dialect_id)
	for content in poped_list:
		md.add(dialect_id, content)

	return md
