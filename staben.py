#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
#import model
from dev import db_commands, debug, decorators
# from dev import debug

# Used for new_password()
import string
import random

app = config.app
render = config.render_template
request = config.request
url_for = config.url_for
session = config.session
flash = config.flash
redirect = config.redirect

debug = debug.debug
async = decorators.async

static_texts = {'nollan': '<span class="nollanfont">minus</span>', 'staben': '<span class="stabenfont">STABEN</span>'}

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

def add_session(db_user):
	config.session['email'] = db_user['user'].email
	config.session['role'] = db_user['user'].role

	if db_user['info'].finished_profile:
		config.session['finished_profile'] = True
	else:
		config.session['finished_profile'] = False

	if db_user['info'].poll_done:
		config.session['poll_done'] = True
	else:
		config.session['poll_done'] = False
	return True

def edit_session(session_value, value):
	config.session[session_value] = value

@app.route('/')
def index():
	return render('index.html', session=session, bla=config.user_roles, st=static_texts)

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
	return render('contact.html', \
		show=show_page, \
		klassforestandare=klassforestandare, \
		studievagledning=studievagledning, \
		st=static_texts)

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

					if not session['finished_profile']:
						redirect_to = 'profile_edit'
					elif not session['poll_done']:
						redirect_to = 'profile_student_poll'
					else:
						redirect_to = 'profile'

					return redirect(url_for(redirect_to, user_email=request.form['email']))
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
		if not db_commands.check_if_email_exist(request.form['email']):
			forbidden_chars = [u'å', u'ä', u'ö']
			forbidden_chars_email = [x for x in forbidden_chars if x in request.form['email']]

			if len(forbidden_chars_email) == 0:
				if request.form['email'] != '' and str(request.form['regCode']) == str(db_commands.get_register_code().code):
					debug('register', 'email och code funkar')
					if request.form['password'] == request.form['rep_password']:
						debug('register', 'Passwords are the same')
						if db_commands.register_user(request.form):
							user = db_commands.get_db_user(db_user_email=request.form['email'], db_user_password=request.form['password'])['user']

							if user:
								if db_commands.add_user_information(user.id):
									debug('register', 'Registration succeeded')
									user = db_commands.get_db_user(user_id=user.id)
									add_session(user)
									return redirect(url_for('profile_edit', user_email=user['user'].email))
								else:
									debug('register', 'Error, could not add user information')
									return redirect(url_for('register'))
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
				debug('register', 'Error, the user typed a forbidden character as his e-mail')
				flash(u'Din e-post får inte innehålla å, ä eller ö!')
				return redirect(url_for('register'))
		else:
			debug('register', 'Error, the email already exists')
			flash(u'E-posten du angav är redan registrerad!')
			return redirect(url_for('register'))
	else:
		return render('register.html')

@app.route('/forgot_password', defaults={'code': ''}, methods=['POST', 'GET'])
@app.route('/forgot_password/<code>', methods=['POST', 'GET'])
def forgot_password(code=None):
	print db_commands.get_db_user({'id': 1})
	if code:
		recover_user = db_commands.get_recover_user(code)
		if recover_user:
			new_password = random_string()
			new_password_bcrypt = config.bcrypt.generate_password_hash(new_password)
			recover_code_md = config.MultiDict([('recover_code', '')])
			print recover_user
			# db_commands.update_db_user(request.form['email'], recover_code_md)
		else:
			return 'NOOOPE'
	if request.method == 'POST':
		if db_commands.check_if_email_exist(request.form['email']):
			if request.form['email'] != '':
				# Send en e-mail to request.form['email'] with an url that will reset the user's password
				recover_code = random_string(25)
				body = '''<b>Hej nollan!</b>
					<br />
					Tryck <a href='http://www.staben.info/forgot_password/%s' target='_blank'>här</a> för att få nytt lösenord på www.staben.info
					<br /><br />
					<b>OBS! Om du ej har förfrågat att få ditt lösenord återställt kan du bortse från detta e-brev!</b>
					''' % (recover_code)
				if send_email([request.form['email']], 'Glömt lösenord på staben.info', html_body=body):
					recover_code_md = config.MultiDict([('recover_code', recover_code)])
					db_commands.update_db_user(request.form['email'], recover_code_md)

					flash(u'Ett e-post har blivit skickad till %s med en återställningslänk som du måste följa för att återställa ditt lösenord.' % (request.form['email']))
					return render('forgot_password.html')
			else:
				flash(u'Du måste ange en e-post.')
				return render('forgot_password.html')
		else:
			flash(u'Den angivna e-posten finns inte i databasen.')
			return render('forgot_password.html')
	else:
		return render('forgot_password.html')

def random_string(length=12):
	lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(length)]
	return ''.join(lst)

def send_email(recipients, subject, email_body=None, html_body=None):
	try:
		msg = config.Message(subject)
		msg.recipients = recipients
		if email_body:
			msg.body = email_body
		elif html_body:
			msg.html = html_body
		send_async_email(msg)
		return True
	except:
		return False

@async
def send_async_email(msg):
	config.mail.send(msg)

'''
	*
	* User profile
	*
'''
@app.route('/profile', defaults={'user_email': ''})
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
		school_programs = db_commands.get_school_programs()
		return render('profile_edit.html', \
			user=user['user'], \
			user_info=user['info'], \
			school_programs=school_programs,
			school_classes=db_commands.get_school_classes(), \
			st=static_texts)
	else:
		return render('login.html', login=False)

# @app.route('/profile/<user_email>/save', defaults={'user_email': ''})
@app.route('/profile/<user_email>/save/', methods=['POST'])
def profile_save(user_email):
	if session and user_email == session['email']:
		if request.form['firstname'] != '' and request.form['lastname'] != '':
			copy_request_form = request.form.copy()
			copy_request_form.add('phonenumber_vis', 1 if 'phonenumber_vis' in request.form else 0)
			copy_request_form.add('finished_profile', 1)

			if session['finished_profile']:
				redirect_to = 'profile'
			else:
				redirect_to = 'profile_student_poll'

			edit_session('finished_profile', True)
			db_commands.update_db_user(user_email, copy_request_form)
			return redirect(url_for(redirect_to, user_email=user_email))
		else:
			return redirect(url_for('profile_edit', user_email=user_email))
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
		school_programs = db_commands.get_user_school_program(user_email)
		return render('profile_class.html', class_mates=class_mates, school_programs=school_programs)
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
			st=static_texts)
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
					edit_session('poll_done', True)
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
	if db_commands.check_role(session['email']) == 0:
		return render('admin_pages.html')
	else:
		return render('admin_fail.html')

@app.route('/admin/addcontact/', methods=['GET', 'POST'])
def admin_addcontact():
	if db_commands.check_role(session['email']) is 0:
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
	if db_commands.check_role(session['email']) is 0:
		users = db_commands.admin_get_all_users()
		return render('admin_get_all_users.html', users=users)
	else:
		return render('admin_fail.html')

@app.route('/admin/student_poll/')
def admin_student_poll():
	if db_commands.check_role(session['email']) is 0:
		return render('admin_student_poll.html', \
			prefixes=db_commands.get_student_poll_prefix(), \
			dialects=db_commands.get_student_poll_dialects())
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
		elif command == 'max_students':
			flash(u'Max antal studenter inlagt.')
			result = db_commands.add_student_poll_max_students(request.form)

		if result:
			# Perhaps add some kind of alert here to show that the
			#  prefix/question was successfully added??
			return redirect(url_for('admin_student_poll'))
		else:
			return 'Couldn\'t add to poll'

@app.route('/admin_student_poll_result')
def admin_student_poll_result():
	if db_commands.check_role(session['email']) is 0:
		return render('admin_student_poll_result.html', \
			users_info=db_commands.admin_get_all_users_w_poll_done(), \
			dialects=db_commands.get_student_poll_dialects(), \
			user_w_points=db_commands.admin_get_top_three_groups())
	else:
		return render('admin_fail.html')

@app.route('/admin_show_student_poll_result/<user_id>')
def admin_show_student_poll_result(user_id):
	if db_commands.check_role(session['email']) is 0:
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
