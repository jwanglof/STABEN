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

def get_class_mates(db_user_email):
	db_user = models.User.query.filter_by(email=db_user_email).first()
	if db_user.r_user_information.school_program > 0:
		return models.User.query.join(models.UserInformation).filter(models.User.role != 0, \
			models.UserInformation.school_program == db_user.r_user_information.school_program).all()
	else:
		return False

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
		return models.User.query.join(models.User.user_information).filter_by(recover_code=recover_code).first()

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

def admin_calc_user_points(user_id, order=False):
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
	answers = models.StudentPollAnswer.query.filter_by(fk_user_id=user_id).all()
	dialects_w_points = config.MultiDict()
	for answer in answers:
		for dialect_id, point in questions_w_dialects_a_points[answer.fk_student_poll_question_id].iteritems():
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
	return models.UserInformation.query.filter_by(poll_done=1).all()

def admin_insert_user_to_group():
	'''
		MultiDict([(DialectID, {UserID: Position})])
		e.g.:
		MultiDict([(1L, {99: 1}, (12L, {99: 3}), (23L, {99: 2})])
	'''

	dialect_md = config.MultiDict()
	rest_md = config.MultiDict()
	student_poll_dialects = get_student_poll_dialects()
	for user_id, content in admin_get_top_groups_users_only().iteritems():
		for i, dialect_id in enumerate(content):
			# Add 1 to i because i starts with 0
			position = i+1

			# Check so there is no more than max_students in a group.
			# If there are more than student_poll_dialects[dialect_id].max_students
			# students they will be added to rest_list to be dealt with later.
			if len(dialect_md.getlist(dialect_id)) < student_poll_dialects[dialect_id-1].max_students:
				dialect_md.add(dialect_id, {user_id: position})
			# If user_id does not exist in dialect_md
			elif not check_if_in_md(dialect_md, user_id):
				# If True it will replace the values
				# If False it will add the value to rest_md
				# if check_if_in_md(dialect_md, user_id, position):
				print '))))))', check_if_in_md(dialect_md, user_id, position)
					# print replace_position_in_md(dialect_md, dialect_id, , {user_id: position})

				# If dialect_id is full in dialect_md,
				# check if the current user_id has a higher position then
				# any of the users already in dialect_md
				#
				# If true, the current user will swap with the user
				# in dialect_md and that user will be added to rest_list
				#
				# If false, the current user will be added to rest_list

				# PROBLEM
				# This adds a user to rest_md EVEN if that user is in dialect_md
				# but with two other positions.
				# E.g.: If a user that has position 1 replaces user2 with position 2, then
				# user2 will be added to rest_md even if user2's position 1 and 3 is in
				# dialect_md
				found = False
				for list_position, ze_list in enumerate(dialect_md.getlist(dialect_id)):
					for list_user_id, list_user_position in ze_list.iteritems():
						if position < list_user_position:
							# replace_position_in_md(dialect_md.getlist(dialect_id), list_user_position, position)
							dialect_md = replace_position_in_md(dialect_md, dialect_id, list_position, \
								{user_id: position})
							print 'Replaced:', {user_id: position}, 'with:', {list_user_id: list_user_position}
							user_id = list_user_id
							found = True
					if found: break #Ugly solution but it works...
				rest_md.add(dialect_id, {user_id: list_user_position})
			# If the user exist in dialect_md
			else:
				print '######', user_id

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
		# dialect_w_total_points_colors = config.OrderedMultiDict()

		# Loop the specific user's top three groups and add to the MultiDict
		for dialect_id, total_point in admin_calc_user_points(i.fk_user_id, True).iteritems():
			if len(dialect_w_total_points) < 3:
				dialect_w_total_points.add(dialect_id, total_point)

				# This is soooo ugly
				# # Gotta find out another way to do this!
				# if not only_users:
				# 	if len(dialect_w_total_points) is 1:
				# 		dialect_w_total_points_colors.add(dialect_id, '#00ff00')
				# 	elif len(dialect_w_total_points) is 2:
				# 		dialect_w_total_points_colors.add(dialect_id, '#ffff00')
				# 	elif len(dialect_w_total_points) is 3:
				# 		dialect_w_total_points_colors.add(dialect_id, '#ff0000')
			else:
				break

		content['top_score'] = dialect_w_total_points
		# content['top_score_colors'] = dialect_w_total_points_colors
		content['user_points'] = admin_calc_user_points(i.fk_user_id)
		content['user'] = get_db_user(user_id=i.fk_user_id)['info']
		top_three_groups[i.fk_user_id] = content
	return top_three_groups

def admin_get_top_groups_users_only(number_of_groups=3):
	top_three_groups = {}
	for i in admin_get_all_users_w_poll_done():
		# content will contain the information gathered
		content = {}

		dialect_w_total_points = config.OrderedMultiDict()

		# Loop the specific user's top three groups and add to the MultiDict
		for dialect_id, total_point in admin_calc_user_points(i.fk_user_id, True).iteritems():
			if len(dialect_w_total_points) < number_of_groups:
				dialect_w_total_points.add(dialect_id, total_point)
			else:
				break

		top_three_groups[i.fk_user_id] = dialect_w_total_points
	return top_three_groups

def sort_dict(m_dict):
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
	tmp_list.reverse()	
	new_omd = config.OrderedMultiDict()
	for a, b in tmp_list:
		new_omd.add(a, b)

	return new_omd

def check_if_in_md(md, user_id, position=None):
	# DialectID: [{UserID: Position}, {UserID: Position}]
	# Loop through the MD
	# Loop through all dicts
	# If user_id is in c (which is a dict) it returns True
	# If position is set it will check if the user's position in the md is higher than the position set
	# E.g. {5: 3} is higher than {5: 2}
	for dialect_id, content in md.iterlists():
		for c in content:
			if user_id in c:
				if position != None:
					print 2222222
					print position, c
					if position < c.get(user_id):
						return c
					else:
						return False
				else:
					return True
	return False

def replace_position_in_md(md, dialect_id, list_position, new_value):
	poped_list = md.getlist(dialect_id)
	poped_list.pop(list_position)
	poped_list.append(new_value)

	md.poplist(dialect_id)
	for content in poped_list:
		md.add(dialect_id, content)

	return md
