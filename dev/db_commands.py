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
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	db_user.firstname = db_user_dict['firstname']
	db_user.lastname = db_user_dict['lastname']
	db_user.phonenumber = db_user_dict['phonenumber']
	db_user.age = db_user_dict['age']
	db_user.facebook_link = db_user_dict['facebook_link']
	db_user.school_class = db_user_dict['school_class']
	db_user.current_city = db_user_dict['current_city']
	db_user.where_from = db_user_dict['where_from']
	db.session.commit()
	# for key,value in db_user_dict.iteritems():
	# 	db_user.key = value
	# Doesnt work.....