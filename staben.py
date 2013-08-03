#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
#import model
from dev import db_commands
from dev import debug

app = config.app
render = config.render_template
request = config.request
url_for = config.url_for
session = config.session
flash = config.flash
redirect = config.redirect

debug = debug.debug

nollan = 'minus'

# DEV OPTIONS
# NEEDS TO BE REMOVED IN PRODUCTION MODE
@app.route('/db_all')
def db_all():
	try:
		db_create()
		db_programs()
		db_classes()
		db_contacts()
		db_code()
		db_student_poll()
		return 'SUUUUUUUUCCESS!!!!!'
	except:
		return 'NOOOOOO SUUUUUUUUCCESS!!!!!!!'

@app.route('/db_create')
def db_create():
	return db_commands.create_db()
@app.route('/db_delete')
def db_delete():
	return db_commands.delete_db()
@app.route('/db_admins')
def db_admins():
	return db_commands.create_admin_users()
@app.route('/db_programs')
def db_programs():
	return db_commands.create_school_programs()
@app.route('/db_classes')
def db_classes():
	return db_commands.create_school_classes()
@app.route('/db_contacts')
def db_contacts():
	return db_commands.create_contacts()
@app.route('/db_code')
def db_code():
	return db_commands.create_secret_code()
@app.route('/db_student_poll')
def db_student_poll():
	return db_commands.create_student_poll()

@app.route('/')
def index():
	return render('index.html', session=session, bla=config.user_roles, nollan=nollan)

@app.route('/prices')
def prices():
	return render('prices.html')

@app.route('/schedule')
@app.route('/schedule/<show_week>')
def schedule(show_week='1'):
	schedule = db_commands.get_schedule(show_week)
	return render('schedule.html', week=show_week, schedule=schedule)

@app.route('/gallery')
def gallery():
	return render('gallery.html')

@app.route('/blog')
def blog():
	return render('blog.html')

@app.route('/contact')
@app.route('/contact/<show_page>')
def contact(show_page='contact'):
	role_klass = 0
	role_studie = 1
	klassforestandare = db_commands.get_contacts(role_klass)
	studievagledning = db_commands.get_contacts(role_studie)
	return render('contact.html', show=show_page, klassforestandare=klassforestandare, studievagledning=studievagledning)

@app.route('/user/login', methods=['POST'])
def login():
	if request.form['email'] not in session:
		if request.method == 'POST':
			user = db_commands.get_db_user(db_user_email=request.form['email'], db_user_password=request.form['password'])

			if user:
				# user_info['user'] contains email, password and role (from the table users)
				# user_info['info'] contains all the user's information (from the table userInformation)
				if add_session(user):
					db_commands.add_login_count(request.form['email'])
					return redirect(url_for('profile', user_email=request.form['email']))
			else:
				return render('login.html', login=False)
		else:
			# return render('profile.html', user_info=user_info, user_role=config.user_roles[user_info.role])
			return redirect(url_for('profile', user_email=request.form['email']))
	return render('login.html', login=False)

@app.route('/user/signout')
def signout():
	session.clear()
	return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		if request.form['email'] != '' and str(request.form['regCode']) == str(db_commands.get_register_code().code):
			debug('register', 'email och code funkar')
			if request.form['password'] == request.form['rep_password']:
				debug('register', 'Passwords are the same')
				if db_commands.register_user(request.form):
					debug('register', 'Registration succeeded')
					user = db_commands.get_db_user(db_user_email=request.form['email'], db_user_password=request.form['password'])

					if user:
						db_commands.add_user_information(user.id)
						add_session(user)
						return redirect(url_for('profile_edit', user_email=user.email))
					else:
						debug('register', 'Error, could not get user')
						return redirect(url_for('register'))
				else:
					debug('register', 'Error, could not register user')
					return redirect(url_for('register'))
			else:
				debug('register', 'Error, the password did not match')
				flash(u'Du måste ange samma lösenord i båda rutorna.')
				return redirect(url_for('register'))
		else:
			debug('register', 'Error, the user did not type his email and register code')
			flash(u'Du måste ange din e-mail och registreringskod!')
			return redirect(url_for('register'))
	else:
		return render('register.html')
	# 	classes = db_commands.get_school_classes()
	# 	return render('register.html', classes=classes)

def add_session(db_user):
	config.session['email'] = db_user.email
	config.session['role'] = db_user.role
	return True

'''
	*
	* User profile
	*
'''
@app.route('/profile/', defaults={'user_email': ''})
@app.route('/profile/<user_email>/')
def profile(user_email):
	if session and user_email == session['email']:
		user = db_commands.get_db_user(db_user_email=user_email)
		return render('profile.html', user=user['user'], user_info=user['info'])
		#return render('profile.html', user_info=user_info, user_role=config.user_roles[user_info.role])
	else:
		return render('login.html', login=False)

#@app.route('/profile/<user_email>/edit', defaults={'user_email': ''})
@app.route('/profile/<user_email>/edit/')
def profile_edit(user_email):
	if session and user_email == session['email']:
		user = db_commands.get_db_user(db_user_email=session['email'])
		classes = db_commands.get_school_classes()
		return render('profile_edit.html', \
			user=user['user'], \
			user_info=user['info'], \
			school_classes=classes)
	else:
		return render('login.html', login=False)

# @app.route('/profile/<user_email>/save', defaults={'user_email': ''})
@app.route('/profile/<user_email>/save/', methods=['POST'])
def profile_save(user_email):
	if session and user_email == session['email']:
		# Need this check since checkboxes doesn't return anything if it's unchecked!
		phonenumber_vis = 0
		if 'phonenumber_vis' in request.form:
			phonenumber_vis = 1
		db_commands.update_db_user(user_email, request.form, phonenumber_vis)
		return redirect(url_for('profile', user_email=user_email))
	else:
		return render('login.html', login=False)

@app.route('/profile/<user_email>/save/password', methods=['POST'])
def profile_save_password(user_email):
	if session and user_email == session['email']:
		if db_commands.update_db_pw(user_email, request.form):
			return redirect(url_for('profile', user_email=user_email))
		else:
			return "Not updated"
	else:
		return render('login.html', login=False)

@app.route('/profile/<user_email>/class/')
def profile_class(user_email):
	if session and user_email == session['email']:
		class_mates = db_commands.get_class_mates(user_email)
		school_class = db_commands.get_school_class(user_email)
		return render('profile_class.html', class_mates=class_mates, school_class=school_class)
	else:
		return render('login.html', login=False)

@app.route('/profile/<user_email>/student_poll/')
def profile_student_poll(user_email):
	if session and user_email == session['email']:
		user = db_commands.get_db_user(db_user_email=session['email'])

		student_poll_user_answers = config.MultiDict([])
		for index, value in enumerate(db_commands.get_student_poll_answers(user_email)):
			student_poll_user_answers.add(int(value), index)

		return render('profile_student_poll.html', \
			student_poll_prefixes=db_commands.get_student_poll_prefix(), \
			student_poll_questions=db_commands.get_student_poll_question(), \
			user_poll_done=user['info'].poll_done, \
			student_poll_user_answers=student_poll_user_answers, \
			nollan=nollan)
	else:
		return render('login.html', login=False)

@app.route('/profile/<user_email>/save/student_poll/', methods=['POST'])
def profile_save_student_poll(user_email):
	if session and user_email == session['email']:
		# Check if the user already have done the student poll
		# Added this check so that no body tries to save his poll more than once
		if db_commands.get_db_user(db_user_email=session['email'])['info'].poll_done == 0:
			if db_commands.update_db_user(user_email, config.ImmutableMultiDict([('poll_done', u'1')])):
				if db_commands.save_student_poll(user_email, request.form):
					return redirect(url_for('profile_student_poll', user_email=user_email))
				else:
					debug('profile_save_student_poll', 'Could not save the student poll')
					return redirect(url_for('profile_student_poll', user_email=user_email))
			else:
				debug('profile_save_student_poll', 'Could not update poll_done on user')
				return redirect(url_for('profile_student_poll', user_email=user_email))
		else:
			return redirect(url_for('profile_student_poll'))
	else:
		return render('login.html', login=False)

'''
	*
	* Admin tools
	*
'''
@app.route('/admin/pages/')
def admin_pages():
	# Need to check that the user is signed in and is an admin
	if db_commands.admin_check(session['email']) == 0:
		return render('admin_pages.html')
	else:
		return render('admin_fail.html')

@app.route('/admin/addcontact/', methods=['GET', 'POST'])
def admin_addcontact():
	if db_commands.admin_check(session['email']) is 0:
		if request.method == 'POST':
			result = db_commands.add_contact(request.form['name'], request.form['phonenumber'],
											 request.form['email'],request.form['role'],
											 request.form['school_class'], request.form['studie_link'])
			return render('admin_addcontact.html', result=result)
		elif request.method == 'GET':
			return render('admin_addcontact.html')
	else:
		return render('admin_fail.html')

@app.route('/admin/users/')
def admin_get_all_users():
	# Need to check that the user is signed in and is an admin
	if db_commands.admin_check(session['email']) is 0:
		users = db_commands.admin_get_all_users()
		return render('admin_get_all_users.html', users=users)
	else:
		return render('admin_fail.html')

@app.route('/admin/student_poll/')
def admin_student_poll():
	if db_commands.admin_check(session['email']) is 0:
		return render('admin_student_poll.html', prefixes=db_commands.get_student_poll_prefix())
	else:
		return render('admin_fail.html')

@app.route('/admin/student_poll/save/<command>', methods=['POST'])
def admin_student_poll_save(command):
	if request.method == 'POST':
		if command == 'prefix':
			flash('Prefix inlagt.')
			result = db_commands.add_student_poll_prefix(request.form)
		elif command == 'question':
			flash(u'Fråga inlagd.')
			result = db_commands.add_student_poll_question(request.form)

		if result:
			# Perhaps add some kind of alert here to show that the
			#  prefix/question was successfully added??
			return redirect(url_for('admin_student_poll'))
		else:
			return 'Couldn\'t add to poll'

@app.route('/admin_student_poll_result')
def admin_student_poll_result():
	if db_commands.admin_check(session['email']) is 0:
		# print db_commands.admin_get_top_three_groups()[1]['user'].firstname
		return render('admin_student_poll_result.html', \
			users_info=db_commands.admin_get_all_users_w_poll_done(), \
			dialects=db_commands.get_student_poll_dialects(), \
			user_w_points=db_commands.admin_get_top_three_groups())
	else:
		return render('admin_fail.html')

@app.route('/admin_show_student_poll_result/<user_id>')
def admin_show_student_poll_result(user_id):
	if db_commands.admin_check(session['email']) is 0:
		alot_of_info = db_commands.admin_get_user_poll_answer(user_id)
		return render('admin_student_poll_user_result.html', \
			user=alot_of_info[1], \
			alot_of_info=alot_of_info[2], \
			dialects=db_commands.get_student_poll_dialects(), \
			number_of_dialects=len(db_commands.get_student_poll_dialects()), \
			user_points=db_commands.admin_calc_user_points(user_id))
	else:
		return render('admin_fail.html')

@app.route('/admin_insert_user_to_group', methods=['POST'])
def admin_insert_user_to_group():
	if request.method == 'POST':
		db_commands.admin_insert_user_to_group()
		flash(u'ALLA ANVÄNDARE HAR EN EGEN GRUPP. WOOOOOOHOOOOOOOOOO!!')
		return redirect(url_for('admin_student_poll'))

@app.teardown_appcontext
def shutdown_session(exception=None):
	config.db_session.remove()

if __name__ == '__main__':
	app.run(host=config.HOST, debug=config.DEBUG)
