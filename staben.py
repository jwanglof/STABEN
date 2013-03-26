#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
#import model
from dev import db_commands

app = config.app
render = config.render_template
get_form = config.request
url_for = config.url_for

# DEV OPTIONS
# NEEDS TO BE REMOVED IN PRODUCTION MODE
@app.route('/db_create')
def db_create():
	return db_commands.create_app()
@app.route('/db_admins')
def db_admins():
	return db_commands.create_admin_users()
@app.route('/db_school')
def db_school():
	return db_commands.create_school_classes()

@app.route('/')
def index():
	return render('index.html', session=config.session, bla=config.user_roles)

@app.route('/prices')
def prices():
	return render('prices.html')

@app.route('/schedule')
def schedule():
	return render('schedule.html')

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
	return render('contact.html', show=show_page)


@app.route('/user/login', methods=['POST'])
def login():
	if get_form.form['email'] not in config.session:
		if config.request.method == 'POST':
			user_info = db_commands.get_db_user(get_form.form['email'],get_form.form['password'])
			if (user_info):
				db_commands.user_signed_in(user_info.email)
				return render('profile.html', user_info=user_info, user_role=config.user_roles[user_info.role])
			else:
				return render('login.html', login=False)
	else:
		return render('profile.html', user_info=user_info, user_role=config.user_roles[user_info.role])
	return render('login.html', login=False)

@app.route('/profile/', defaults={'user_email': ''})
@app.route('/profile/<user_email>')
def profile(user_email):
	if config.session and user_email == config.session['email']:
		user_info = db_commands.get_db_user(config.session['email'])
		return render('profile.html', user_info=user_info, user_role=config.user_roles[user_info.role])
	else:
		return render('login.html', login=False)

@app.route('/profile/<user_email>/edit', defaults={'user_email': ''})
@app.route('/profile/<user_email>/edit')
def profile_edit(user_email):
	if config.session and user_email == config.session['email']:
		user_info = db_commands.get_db_user(config.session['email'])
		classes = db_commands.get_school_classes()
		return render('profile_edit.html', user_info=user_info, school_classes=classes, school_class=int(user_info.school_class))
	else:
		return render('login.html', login=False)

@app.route('/profile/<user_email>/save', defaults={'user_email': ''})
@app.route('/profile/<user_email>/save', methods=['POST'])
def profile_save(user_email):
	if config.session and user_email == config.session['email']:
		print('/save - HEJENSA')
		db_commands.update_db_user(user_email, get_form.form)
		return config.redirect(url_for('profile', user_email=user_email))
	else:
		return render('login.html', login=False)

'''@app.route('/user/profile')
def profile():
	if config.session:
		user_info = db_commands.get_db_user(config.session['email'])
		return render('profile.html', user_info=user_info, user_role=config.user_roles[user_info.role])
	else:
		return render('login.html', login=False)

@app.route('/user/edit/<path:save>', methods=['GET','POST'])
def edit(save):
	print(save)
	if config.session:
		user_info = db_commands.get_db_user(config.session['email'])
		classes = db_commands.get_school_classes()
		return render('profile_edit.html', user_info=user_info, school_classes=classes)
	else:
		return render('login.html', login=False)

@app.route('/user/edit/save', methods=['POST'])
def edit_user():
	print db_commands.update_db_user(config.session['email'], get_form.form)
	#return config.redirect(url_for('profile'))
	

@app.route('/user/edit/save/password', methods=['POST'])
def edit_password():
	return 'bajsa'''

@app.route('/user/signout')
def signout():
	config.session.clear()
	return config.redirect(url_for('index'))


if __name__ == '__main__':
	app.debug = True
	app.run()
