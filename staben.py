#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
#import model
from dev import db_commands

app = config.app
render = config.render_template
request = config.request
url_for = config.url_for
session = config.session
flash = config.flash

nollan = 'minus'

def login_user(user_email, user_password):
	user = db_commands.get_db_user(user_email, user_password)

	if user:
		# user_info['user'] contains email, password and role (from the table users)
		# user_info['info'] contains all the user's information (from the table userInformation)
		#db_commands.login_count(request.form['email'])
		
		return user
	else:
		# return render('login.html', login=False)
		return False

# DEV OPTIONS
# NEEDS TO BE REMOVED IN PRODUCTION MODE
@app.route('/db_create')
def db_create():
	return db_commands.create_db()
@app.route('/db_admins')
def db_admins():
	return db_commands.create_admin_users()
@app.route('/db_school')
def db_school():
	return db_commands.create_school_classes()
@app.route('/db_contacts')
def db_contacts():
	return db_commands.create_contacts()

@app.route('/')
def index():
	return render('index.html', session=session, bla=config.user_roles, nollan=nollan)

@app.route('/prices')
def prices():
	return render('prices.html')

@app.route('/schedule')
@app.route('/schedule/<show_week>')
def schedule(show_week='1'):
	schedule_date = db_commands.get_schedule(show_week)
	return render('schedule.html', week=show_week, schedule=schedule_date)

@app.route('/student_poll')
def student_poll():
	return render('student_poll.html')

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
			user = db_commands.get_db_user(request.form['email'], request.form['password'])

			if user:
				# user_info['user'] contains email, password and role (from the table users)
				# user_info['info'] contains all the user's information (from the table userInformation)
				db_commands.login_count(request.form['email'])
				return config.redirect(url_for('profile', user_email=request.form['email']))
			else:
				return render('login.html', login=False)
		else:
			# return render('profile.html', user_info=user_info, user_role=config.user_roles[user_info.role])
			return config.redirect(url_for('profile', user_email=request.form['email']))
	return render('login.html', login=False)

@app.route('/profile/', defaults={'user_email': ''})
@app.route('/profile/<user_email>/')
def profile(user_email):
	if session and user_email == session['email']:
		user = db_commands.get_db_user(user_email)
		return render('profile.html', user=user['user'], user_info=user['info'])
		#return render('profile.html', user_info=user_info, user_role=config.user_roles[user_info.role])
	else:
		return render('login.html', login=False)

#@app.route('/profile/<user_email>/edit', defaults={'user_email': ''})
@app.route('/profile/<user_email>/edit/')
def profile_edit(user_email):
	if session and user_email == session['email']:
		user = db_commands.get_db_user(session['email'])
		#user_info = db_commands.get_user_info()
		classes = db_commands.get_school_classes()
		return render('profile_edit.html', user=user['user'], user_info=user['info'], school_classes=classes)
	else:
		return render('login.html', login=False)

# @app.route('/profile/<user_email>/save', defaults={'user_email': ''})
@app.route('/profile/<user_email>/save/', methods=['POST'])
def profile_save(user_email):
	if session and user_email == session['email']:
		'''
			Need this check since checkboxes doesn't return anything if it's unchecked!
		'''
		phonenumber_vis = 0
		if 'phonenumber_vis' in request.form:
			phonenumber_vis = 1

		db_commands.update_db_user(user_email, request.form, phonenumber_vis)
		return config.redirect(url_for('profile', user_email=user_email))
	else:
		return render('login.html', login=False)

@app.route('/profile/<user_email>/save/password', methods=['POST'])
def profile_password(user_email):
	if session and user_email == session['email']:
		if db_commands.update_db_pw(user_email, request.form):
			return config.redirect(url_for('profile', user_email=user_email))
		else:
			return "Not updated"
	else:
		return render('login.html', login=False)

@app.route('/profile/<user_email>/class/')
def profile_class(user_email):
	if session and	user_email == session['email']:
		class_mates = db_commands.get_class_mates(user_email)
		school_class = db_commands.get_school_class(user_email)
		return render('profile_class.html', class_mates=class_mates, school_class=school_class)
	else:
		return render('login.html', login=False)

@app.route('/user/signout')
def signout():
	session.clear()
	return config.redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		print 'POST'
		regCode = request.form['regCode']
		code = db_commands.get_register_code()
		if request.form['email'] != '' and str(regCode) == str(code):
			print 'email och code funkar'
			if request.form['password'] == request.form['rep_password']:
				# print db_commands.register_user(request.form)
				if db_commands.register_user(request.form):
					user = login_user(request.form['email'], request.form['password'])
					if user:
						db_commands.add_user_information(user.id)
						return config.redirect(url_for('profile_edit', user_email=user.email))
					else:
						print 'Unsuccessfull, user is None'
				else:
					print 'Unsuccessfull, could not register user'
			else:
				flash(u'Du måste ange samma lösenord i båda rutorna.')
		else:
			flash(u'Du måste ange din e-mail och registreringskod!')
	else:
		return render('register.html')
	# 	classes = db_commands.get_school_classes()
	# 	return render('register.html', classes=classes)

'''
	*
	* Admin tools
	*
'''
@app.route('/admin/pages')
def admin_pages():
	# Need to check that the user is signed in and is an admin
	if db_commands.admin_check(session['email']) == 0:
		return render('admin_pages.html')
	else:
		return render('admin_fail.html')

@app.route('/admin/addcontact', methods=['GET', 'POST'])
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

@app.route('/admin/users')
def admin_users():
	# Need to check that the user is signed in and is an admin
	if db_commands.admin_check(session['email']) is 0:
		users = db_commands.admin_users()
		return render('admin_users.html', users=users)
	else:
		return render('admin_fail.html')

if __name__ == '__main__':
	app.debug = True
	app.run()