import model
import config

db = config.db
app = config.app

# Should check if the DB is created successfully or not!
def create_app():
	#db.init_app(app)
	#with app.test_request_context():
	db.create_all()
	return "Done"

def create_admin_users():
    	db.session.add(model.waeggen_user)
    	#db.session.add(model.simba_user)
    	db.session.commit()