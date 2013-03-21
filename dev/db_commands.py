import model
import config

db = config.db
app = config.app

# initial users
admin_users = []
admin_users.append(model.Users('jwanglof@gmail.com', 'tmppass', 'Johan', 'Wanglof', 'WebmastAH', '0046708601911', 1))
admin_users.append(model.Users('simis.linden@gmail.com', 'tmppass', 'Simon', 'Linden', 'WebmastAH', '0046735026994', 1))

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
		if db_user_password is not None:
			# pw_hash = config.bcrypt.generate_password_hash(db_user_password)
			# config.bcrypt.check_password_hash(pw_hash, db_user_password)
			db_pass = model.Users.query.filter_by(password=db_user_password).first()
			if db_pass != None:
				config.session['email'] = db_user_email
				return "TRUE"
			else:
				return "FALSE"
		else:
			return db_user
	else:
		return "NOOOPE"
