#!/usr/bin/python
# -*- coding: utf-8 -*-

import model
import config

db = config.db
app = config.app

# initial users
admin_users = []
admin_users.append(model.Users('jwanglof@gmail.com', 'tmppass', 'WebmastAH', 0, 'Johan', 'Wanglof', '0046708601911', 0))
admin_users.append(model.Users('simis.linden@gmail.com', 'tmppass', 'WebmastAH', 0, 'Simon', 'Linden', '0046735026994', 0))

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
	return "DB creation done"

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

def update_db_user(db_user_email, db_user_dict, phonenumber_vis):
	print(db_user_dict, phonenumber_vis)

	print(1)
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	print(2)
	db_user.firstname = db_user_dict['firstname']
	print(3)
	db_user.lastname = db_user_dict['lastname']
	print(4)
	db_user.phonenumber = db_user_dict['phonenumber']
	print(5)
	db_user.phonenumber_vis = phonenumber_vis
	print(6)
	db_user.age = db_user_dict['age']
	print(7)
	db_user.facebook_url = db_user_dict['facebook_url']
	print(8)
	db_user.school_class = db_user_dict['school_class']
	print(9)
	db_user.current_city = db_user_dict['current_city']
	print(0)
	db_user.where_from = db_user_dict['where_from']
	db_user.presentation = db_user_dict['presentation']
	print(1)
	db.session.commit()
	# for key,value in db_user_dict.iteritems():
	# 	db_user.key = value
	# Doesnt work.....
	return True

def user_signed_in(db_user_email):
	#model.Users.query.filter_by(email=db_user_email).first().update({times_signed_in: times_signed_in+1})
	#db.session.execute(update(db_user, values={times_signed_in: times_signed_in+1}))
	#db.session.
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	db_user.times_signed_in = db_user.times_signed_in+1
	db.session.commit()

def get_school_classes():
	return model.SchoolClasses.query

def get_class_mates(db_user_email):
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	class_mates = model.Users.query.filter_by(school_class=db_user.school_class).all()
	return class_mates

def get_school_class(db_user_email):
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	school_class = model.SchoolClasses.query.filter_by(id=db_user.school_class).first()
	return school_class.abbreviation