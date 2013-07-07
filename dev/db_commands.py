#!/usr/bin/python
# -*- coding: utf-8 -*-

import models
import config

import read_csv
import debug

db = config.db
app = config.app
db_session = config.db_session

debug = debug.debug

import locale
debug('locale', str(locale.getdefaultlocale()))

import os

# initial users
admin_users2 = []
admin_users2.append(models.Users('jwanglof@gmail.com', 'tmppass', 0))
admin_users2.append(models.Users('simis.linden@gmail.com', 'tmppass', 0))

admin_users_info = []
admin_users_info.append(models.UserInformation('Johan'))
admin_users_info.append(models.UserInformation('Simon'))

school_classes = []
school_classes.append(models.SchoolClasses('D', 'Datateknik'))
school_classes.append(models.SchoolClasses('IT', 'Informationsteknologi'))
school_classes.append(models.SchoolClasses('IP', 'Innovativ Programmering'))
school_classes.append(models.SchoolClasses('U', 'Mjukvaruteknik'))

contacts = []
contacts.append(models.Contacts('Patrik Hillgren', '070-0434527', 'pathi747@student.liu.se', 0, 'IT0',''))
contacts.append(models.Contacts('Alicia Tonolli', '070-4237004', 'alito938@student.liu.se', 0, 'D0a',''))
contacts.append(models.Contacts('Johan Falk', '070-8468608', 'johfa808@student.liu.se', 0, 'D0b',''))
contacts.append(models.Contacts('Tony Fredriksson', '070-6745520', 'tonfr314@student.liu.se', 0, 'D0c',''))
contacts.append(models.Contacts('Gustav Bylund', '073-0262686', 'gusby403@student.liu.se', 0, 'IP0',''))
contacts.append(models.Contacts('Alex Telon', '070-2647531', 'alete471@student.liu.se', 0, 'U0',''))
contacts.append(models.Contacts('Siv Söderlund', '013-282836', 'siv.soderlund@liu.se', 1, '', 'http://www.liu.se/personal/tfk/sivso41?l=sv'))

schedule_date = []
schedule_date.append(models.ScheduleDate('1', '20/8', 'Tisdag', '1a', '../static/img/schedule_tisdag20_tmp.PNG',
										'07:00 - 18:00', 'Folkets park, Campushallen, universitetet',
										'Idag är det dags för minus att träffa andra minus och faddrar på parkeringen till Folkets park kl 7.00. Här kommer minus träffa D-group och CC som kommer lära minus att sjunga sin nollesång på yppersta och fagraste sätt.Därefter kommer minus att tåga vidare till Campushallen för att bli underhållna och se STABEN. Superskojsigt,  minus!',
										'Därefter kommer minus att vandra mot universitetet. Därför är det dumt om minus har sin cykel med sig, då minus inte kommer att cykla. STABEN rekommenderar därför att minus lämnar cykeln hemma. Resten av dagen kommer minus att bli uppropad, indelad, tilldelad, föreläst för och utfrågad. Uppropad för att universitetet ska se så att minus är där minus bör vara, Linkeboda ju, indelad för att minus ska få en klass, föreläst för att minus ska lära sig saker och utfrågad för att minus ska ha det roligt i nolle-p. Minus har en lång dag framför sig, så minus bör vara väl utvilad och dessutom ta med sig en frukt eller smörgås.'))

# Should check if the DB is created successfully or not!
def create_db():
	config.Base.metadata.create_all(bind=config.engine)
	return "DB creation done"

def create_admin_users():
	# TODO: Call to register_user instead with a dict!!
	for admin in admin_users2:
		db_session.add(admin)

	'''for admin_info in admin_users_info:
		db_session.add(admin_info)'''

	db_session.commit()
	return "Admin users added"

def create_secret_code():
	db_session.add(models.RegisterCode('asd'))
	db_session.commit()
	return 'Secret code added'
	# Add the secret code to the DB!
	# two_weevil

def create_school_classes():
	for classes in school_classes:
		db_session.add(classes)
	db_session.commit()
	return "School classes added"

def create_contacts():
	for contact in contacts:
		db_session.add(contact)
	db_session.commit()
	return "Contacts added"

def create_student_poll():
	StudentPoll = read_csv.ReadStudentPollCsvFile(os.getcwd() + '/studentpoll.csv')

	# Add prefixes
	for index, p in StudentPoll.get_prefixes().iteritems():
		db_session.add(models.StudentPollPrefix(index, p))

	# Add questions
	for index, dict_content in StudentPoll.get_questions().iteritems():
		for q in dict_content:
			db_session.add(models.StudentPollQuestion(index, q))

	# Add dialects
	for index, d in StudentPoll.get_dialects().iteritems():
		db_session.add(models.StudentPollDialect(index, d))

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

# def gen_pw(clear_pw):
# 	return config.bcrypt.generate_password_hash(clear_pw)

def add_contact(name, phonenumber, email, role, school_class, link):
	contact = models.Contact(name, phonenumber, email, role, school_class, link)
	db_session.add(contact)
	db_session.commit()
	return 'success'

def add_login_count(db_user_email):
	db_user = models.Users.query.filter_by(email=db_user_email).first()
	user_info = models.UserInformation.query.filter_by(fk_user_id=db_user.id).first()
	user_info.login_count += 1
	db_session.commit()

def add_user_information(db_user_id):
	db_session.add(models.UserInformation(db_user_id))
	db_session.commit()
	return True

def get_class_mates(db_user_email):
	db_user = models.Users.query.filter_by(email=db_user_email).first()
	user_info = models.UserInformation.query.filter_by(fk_user_id=db_user.id).first()
	class_mates = models.UserInformation.query.filter_by(school_class=user_info.school_class).all()
	return class_mates

def get_contacts(role):
	if role is 0:
		contacts = models.Contacts.query.filter_by(role=role).order_by(models.Contacts.school_class).all()
	else:
		contacts = models.Contacts.query.filter_by(role=role).all()
	return contacts

def get_db_user(user_id=None,db_user_email=None,db_user_password=None):
	if db_user_email != None:
		db_user = models.Users.query.filter_by(email=db_user_email).first()
	elif user_id != None:
		db_user = models.Users.query.filter_by(id=user_id).first()

	if db_user is not None:
		db_user_info = {'user': db_user, 'info': models.UserInformation.query.filter_by(fk_user_id=db_user.id).first()}

		# Check to see if a user is signing in
		if db_user_password is not None:
			if config.bcrypt.check_password_hash(db_user.password, db_user_password):
				config.session['email'] = db_user_email
				config.session['role'] = db_user.role

				return db_user
			else:
				return False
		else:
			return db_user_info
	else:
		return False

def get_register_code():
	return models.RegisterCode.query.first()

def get_schedule(week):
	return models.ScheduleDate.query.filter_by(week=week).order_by(models.ScheduleDate.week).all()

def get_school_class(db_user_email):
	db_user = models.Users.query.filter_by(email=db_user_email).first()
	user_info = models.UserInformation.query.filter_by(fk_user_id=db_user.id).first()
	school_class = models.SchoolClasses.query.filter_by(id=user_info.school_class).first()
	return school_class.abbreviation

def get_school_classes():
	return models.SchoolClasses.query

def get_student_poll_answers(db_user_email):
	user_id = get_db_user(db_user_email=db_user_email)['user'].id
	return models.StudentPollAnswer.query.filter_by(fk_user_id=user_id).order_by(models.StudentPollAnswer.id).all()

def get_student_poll_dialects():
	return models.StudentPollDialect.query.order_by(models.StudentPollDialect.id).all()

def get_student_poll_points():
	return models.StudentPollPoint.query.order_by(models.StudentPollPoint.fk_student_poll_question_id).all()

def get_student_poll_prefix():
	return models.StudentPollPrefix.query.order_by(models.StudentPollPrefix.id).all()

def get_student_poll_question():
	return models.StudentPollQuestion.query.order_by(models.StudentPollQuestion.id).all()

def register_user(db_user_dict):
	try:
		new_user = models.Users(db_user_dict['email'], config.bcrypt.generate_password_hash(db_user_dict['password']))
		db_session.add(new_user)
		db_session.commit()

		return True
	except:
		return False

def save_student_poll(db_user_email, db_student_poll_dict):
	try:
		db_user = models.Users.query.filter_by(email=db_user_email).first()
		for x in db_student_poll_dict:
			db_session.add(models.StudentPollAnswer(db_user.id, x))
		db_session.commit()
		return True
	except:
		return False

def update_db_user(db_user_email, db_user_dict, phonenumber_vis=None):
	try:
		db_user = models.Users.query.filter_by(email=db_user_email).first()
		models.UserInformation.query.filter_by(fk_user_id=db_user.id).update(db_user_dict)
		if phonenumber_vis != None:
			models.UserInformation.query.filter_by(fk_user_id=db_user.id).update({'phonenumber_vis': phonenumber_vis})
		db_session.commit()
		return True
	except:
		return False

def update_db_pw(db_user_email, db_user_dict):
	db_user = models.Users.query.filter_by(email=db_user_email).first()
	if db_user_dict['new_password'] == db_user_dict['repeat_password'] and db_user_dict['current_password'] == db_user.password:
		models.Users.query.filter_by(email=db_user_email).update({'password': db_user_dict['new_password']})
		db_session.commit()
		return True
	else:
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

def admin_get_all_student_poll_answers():
	# asd = models.StudentPollAnswer.query.order_by(models.StudentPollAnswer.fk_user_id).all()
	# db_user_info = {'user': db_user, 'info': models.UserInformation.query.filter_by(fk_user_id=db_user.id).first()}
	asd = models.StudentPollAnswer.query.order_by(models.StudentPollAnswer.fk_user_id).all()
	return asd

def admin_calc_user_points(user_id):
	points = models.StudentPollPoint.query.all()

	questions_w_points = models.StudentPollQuestion.query.order_by(models.StudentPollQuestion.id).all()

	# {Question_id: {Dialect_id: Point}}
	bla = config.MultiDict()
	for question in questions_w_points:
		point_MD = config.MultiDict()
		for point in question.question_point:
			point_MD.add(point.fk_student_poll_dialect_id, point.point)
		bla.add(question.id, point_MD)

	# {Dialect_id: Total_points}
	answers = models.StudentPollAnswer.query.filter_by(fk_user_id=user_id).order_by(models.StudentPollAnswer.fk_student_poll_question_id).all()
	dialects_w_points = config.MultiDict()	
	# Is the answers from ONLY user_id
	for answer in answers:
		for dialect_id, point in bla[answer.fk_student_poll_question_id].iteritems():
			dialects_w_points.add(dialect_id, point)

	"""
	Add the missing dialect id(s) to dialects_w_points
	"""
	for i in range(1, len(get_student_poll_dialects())+1):
		if not dialects_w_points.get(i):
			dialects_w_points.add(i, 0)

	dsa = {}
	for key, value in dialects_w_points.iteritems(multi=True):
		if key in dsa:
			dsa[key] = dsa[key]+value
		else:
			dsa[key] = value

	return dsa

def admin_get_user_poll_answer(user_id):
	userinfo_w_answers = models.Users.query.filter_by(id=user_id).join(models.Users.user_information).join(models.Users.student_poll).all()
	prefixes_w_questions_w_points = models.StudentPollPrefix.query.order_by(models.StudentPollPrefix.id).all()

	pref_w_ques_w_point_OMD = config.OrderedMultiDict()
	for content in prefixes_w_questions_w_points:
		questions_OMD = config.OrderedMultiDict()
		for question in content.question:
			dialect_id_w_points_OMD = config.OrderedMultiDict()
			for point in question.question_point:
				dialect_id_w_points_OMD.add(point.fk_student_poll_dialect_id, point.point)
			inner_OMD = config.OrderedMultiDict()
			inner_OMD.add('question', question.question)
			inner_OMD.add('points', dialect_id_w_points_OMD)
			questions_OMD.add(question.id, inner_OMD)
		pref_w_ques_w_point_OMD.add(content.prefix, questions_OMD)
	
	userinfo_w_answers_MD = config.MultiDict()
	for userinfo in userinfo_w_answers:
		userinfo_w_answers_MD.add('userinfo', userinfo.user_information)
		for answer in userinfo.student_poll:
			userinfo_w_answers_MD.add(answer.fk_student_poll_question_id, answer.fk_student_poll_question_id)
	#, 4: admin_calc_user_points(user_id)
	return {1: userinfo_w_answers_MD, 2: pref_w_ques_w_point_OMD}

def admin_check(db_user_email):
	# Check only role!
	user_info = models.Users.query.filter_by(email=db_user_email).first()
	return user_info.role

def admin_get_all_users():
	return {'user': models.Users.query.all(), 'info': models.UserInformation.query.all()}

def admin_get_all_users_w_poll_done():
	return models.UserInformation.query.filter_by(poll_done=1).all()