#!/usr/bin/python
# -*- coding: utf-8 -*-

import model
import config

db = config.db
app = config.app

# initial users
admin_users2 = []
admin_users2.append(model.Users('jwanglof@gmail.com', 'tmppass', 0))
admin_users2.append(model.Users('simis.linden@gmail.com', 'tmppass', 0))

admin_users_info = []
admin_users_info.append(model.UserInformation('Johan'))
admin_users_info.append(model.UserInformation('Simon'))

school_classes = []
school_classes.append(model.SchoolClasses('D', 'Datateknik'))
school_classes.append(model.SchoolClasses('IT', 'Informationsteknologi'))
school_classes.append(model.SchoolClasses('IP', 'Innovativ Programmering'))
school_classes.append(model.SchoolClasses('U', 'Mjukvaruteknik'))

contacts = []
contacts.append(model.Contact('Patrik Hillgren', '070-0434527', 'pathi747@student.liu.se', 0, 'IT0',''))
contacts.append(model.Contact('Alicia Tonolli', '070-4237004', 'alito938@student.liu.se', 0, 'D0a',''))
contacts.append(model.Contact('Johan Falk', '070-8468608', 'johfa808@student.liu.se', 0, 'D0b',''))
contacts.append(model.Contact('Tony Fredriksson', '070-6745520', 'tonfr314@student.liu.se', 0, 'D0c',''))
contacts.append(model.Contact('Gustav Bylund', '073-0262686', 'gusby403@student.liu.se', 0, 'IP0',''))
contacts.append(model.Contact('Alex Telon', '070-2647531', 'alete471@student.liu.se', 0, 'U0',''))
contacts.append(model.Contact('Siv Söderlund', '013-282836', 'siv.soderlund@liu.se', 1, '', 'http://www.liu.se/personal/tfk/sivso41?l=sv'))

def generate_password(user_password):
	return 

def check_password(user_password):
	return 

# Should check if the DB is created successfully or not!
def create_db():
	#db.init_app(app)
	#with app.test_request_context():
	db.create_all()
	return "DB creation done"

def create_admin_users():
	# TODO: Call to register_user instead with a dict!!
	for admin in admin_users2:
		db.session.add(admin)

	'''for admin_info in admin_users_info:
		db.session.add(admin_info)'''

	db.session.commit()
	return "Admin users added"

def create_school_classes():
	for classes in school_classes:
		db.session.add(classes)
	db.session.commit()
	return "School classes added"

def create_contacts():
	for contact in contacts:
		db.session.add(contact)
	db.session.commit()
	return "Contacts added"

def get_db_user(db_user_email,db_user_password=None):
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	if db_user is not None:
		db_user_info = {'user': db_user, 'info': model.UserInformation.query.filter_by(user_id=db_user.id)}

		# Check to see if a user is signing in
		#
		# A user wants to sign in
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

def update_db_user(db_user_email, db_user_dict, phonenumber_vis):
	db_user = model.Users.query.filter_by(email=db_user_email).first()

	model.UserInformation.query.filter_by(user_id=db_user.id).update(db_user_dict)
	model.UserInformation.query.filter_by(user_id=db_user.id).update({'phonenumber_vis': phonenumber_vis})

	db.session.commit()

	return True

def login_count(db_user_email):
	#db_user = model.Users.query.filter_by(email=db_user_email).first()
	#user_info = model.UserInformation.query.filter_by(user_id=db_user.id).first()
	#user_info.login_count += 1

	db.session.commit()

def get_school_classes():
	return model.SchoolClasses.query

def get_class_mates(db_user_email):
	db_user = model.Users.query.filter_by(email=db_user_email).first()
	user_info = model.UserInformation.query.filter_by(user_id=db_user.id).first()
	print user_info
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


def add_contact(name, phonenumber, email, role, school_class, link):
	contact = model.Contact(name, phonenumber, email, role, school_class, link)
	db.session.add(contact)
	db.session.commit()
	return 'success'


def admin_check(db_user_email):
	# Check only role!
	user_info = model.Users.query.filter_by(email=db_user_email).first()
	return user_info.role

def admin_users():
	return model.Users.query.all()

def register_user(db_user_dict):
	try:
		db.session.add(model.Users(db_user_dict['email'], config.bcrypt.generate_password_hash(db_user_dict['password'])))
		db.session.commit()
		return True
	except:
		return False

def add_user_information(db_user_id):
	db.session.add(model.UserInformation(db_user_id))
	db.session.commit()
	return True

def get_contacts(role):
	if role is 0:
		contacts = model.Contact.query.filter_by(role=role).order_by(model.Contact.school_class).all()
	else:
		contacts = model.Contact.query.filter_by(role=role).all()
	return contacts
