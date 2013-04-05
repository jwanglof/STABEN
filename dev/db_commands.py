#!/usr/bin/python
# -*- coding: utf-8 -*-

import model
import config

db = config.db
app = config.app

# initial users
admin_users = []
admin_users.append(model.Users('jwanglof@gmail.com', 'tmppass', 0))
admin_users.append(model.Users('simis.linden@gmail.com', 'tmppass', 0))

admin_users_info = []
admin_users_info.append(model.UserInformation('Johan'))
admin_users_info.append(model.UserInformation('Simon'))

school_classes = []
school_classes.append(model.SchoolClasses('D', 'Datateknik'))
school_classes.append(model.SchoolClasses('IT', 'Informations Teknologi'))
school_classes.append(model.SchoolClasses('IP', 'Innovativ Programmering'))
school_classes.append(model.SchoolClasses('U', 'Mjukvaruteknik'))

# Should check if the DB is created successfully or not!
def create_db():
	#db.init_app(app)
	#with app.test_request_context():
	db.create_all()
	return "DB creation done"

def create_admin_users():
	for admin in admin_users:
		db.session.add(admin)

	for admin_info in admin_users_info:
		db.session.add(admin_info)

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
		db_user_info = {'user': db_user, 'info': model.UserInformation.query.filter_by(user_id=db_user.id)}

		# Check to see if a user is signing in
		#
		# A user wants to sign in
		if db_user_password != None:
			if db_user_password == db_user.password:
				config.session['email'] = db_user_email
				config.session['role'] = db_user.role

				return db_user_info
			else:
				return False
		else:
			return db_user_info
	else:
		return False

def update_db_user(db_user_email, db_user_dict, phonenumber_vis):
	# Need to check if a password changes!!!!
	db_user = model.Users.query.filter_by(email=db_user_email).first()

	model.UserInformation.query.filter_by(user_id=db_user.id).update(db_user_dict)
	model.UserInformation.query.filter_by(user_id=db_user.id).update({'phonenumber_vis': phonenumber_vis})

	db.session.commit()

	return True

def user_signed_in(db_user_email):
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	user_info = model.UserInformation.query.filter_by(user_id=db_user.id).first()
	user_info.times_signed_in = user_info.times_signed_in+1
	db.session.commit()

def get_school_classes():
	return model.SchoolClasses.query

def get_class_mates(db_user_email):
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	user_info = model.UserInformation.query.filter_by(user_id=db_user.id).first()
	class_mates = model.UserInformation.query.filter_by(school_class=user_info.school_class).all()

	return class_mates

def get_school_class(db_user_email):
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	user_info = model.UserInformation.query.filter_by(user_id=db_user.id).first()
	school_class = model.SchoolClasses.query.filter_by(id=user_info.school_class).first()
	
	return school_class.abbreviation

def update_db_pw(db_user_email, db_user_dict):
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	if db_user_dict['new_password'] == db_user_dict['repeat_password'] and db_user_dict['current_password'] == db_user.password:
		model.Users.query.filter_by(email=db_user_email).update({'password': db_user_dict['new_password']})
		db.session.commit()
		return True
	else:
		return False

def admin_check(db_user_email):
	# Check only role!
	user_info = model.Users.query.filter_by(email=db_user_email).first()
	return user_info.role

def admin_users():
	return model.Users.query.all()