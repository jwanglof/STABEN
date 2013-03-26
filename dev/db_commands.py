#!/usr/bin/python
# -*- coding: utf-8 -*-

import model
import config

db = config.db
app = config.app

# initial users
admin_users = []
admin_users.append(model.Users('jwanglof@gmail.com', 'tmppass', 'WebmastAH', 0, 'Johan', 'Wanglof', '0046708601911'))
admin_users.append(model.Users('simis.linden@gmail.com', 'tmppass', 'WebmastAH', 0, 'Simon', 'Linden', '0046735026994'))

school_classes = []
school_classes.append(model.SchoolClasses('D', 'Datateknik'))
school_classes.append(model.SchoolClasses('IT', 'Informations Teknologi'))
school_classes.append(model.SchoolClasses('IP', 'Innovativ Programmering'))
school_classes.append(model.SchoolClasses('U', 'Mjukvaruteknik'))

# Should check if the DB is created successfully or not!
def create_app():
	#db.init_app(app)
	#with app.test_request_context():
	db.create_all()
	return "Done"

def create_admin_users():
	for admin in admin_users:
		db.session.add(admin)
	db.session.commit()
	return "Admin users added"

def create_school_classes():
	for classes in school_classes:
		db.session.add(classes)
	db.session.commit()
	return "School classes added"

def gen_pw(clear_pw):
	return config.bcrypt.generate_password_hash(clear_pw)

def get_db_user(db_user_email,db_user_password=None):
	db_user = model.Users.query.filter_by(email=db_user_email).first()

	if db_user != None:
		# Check to see if a user is signing in
		#
		# A user wants to sign in
		if db_user_password is not None:
			# pw_hash = config.bcrypt.generate_password_hash(db_user_password)
			# config.bcrypt.check_password_hash(pw_hash, db_user_password)
			db_pass = model.Users.query.filter_by(password=db_user_password).first()
			if db_pass != None:
				config.session['email'] = db_user_email
				config.session['role'] = db_user.role
				return db_user
			else:
				return False

		# A user's DB information
		else:
			return db_user
	else:
		return False

def update_db_user(db_user_email, db_user_dict):
	print('update_db_user - 1')
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	print('update_db_user - 2')
	db_user.firstname = db_user_dict['firstname']
	print('update_db_user - 3')
	db_user.lastname = db_user_dict['lastname']
	print('update_db_user - 4')
	db_user.phonenumber = db_user_dict['phonenumber']
	print('update_db_user - 5')
	db_user.age = db_user_dict['age']
	print('update_db_user - 6')
	db_user.facebook_link = db_user_dict['facebook_link']
	print('update_db_user - 7')
	db_user.school_class = db_user_dict['school_class']
	print('update_db_user - 8')
	db_user.current_city = db_user_dict['current_city']
	print('update_db_user - 9')
	db_user.where_from = db_user_dict['where_from']
	print('update_db_user - 0')
	db.session.commit()
	print('asddwqasd')
	# for key,value in db_user_dict.iteritems():
	# 	db_user.key = value
	# Doesnt work.....
	return "DWQDWQD"

def user_signed_in(db_user_email):
	#model.Users.query.filter_by(email=db_user_email).first().update({times_signed_in: times_signed_in+1})
	#db.session.execute(update(db_user, values={times_signed_in: times_signed_in+1}))
	#db.session.
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	db_user.times_signed_in = db_user.times_signed_in+1
	db.session.commit()
	print("BAAAAAJS")

def get_school_classes():
	return model.SchoolClasses.query
