import config
#import model
from dev import db_commands

app = config.app

# DEV OPTIONS
# NEED TO BE REMOVED IN PRODUCTION MODE
@app.route('/db_create')
def db_create():
	return db_commands.create_app()

@app.route('/')
def index():
	return config.render_template('index.html')

@app.route('/contact')
def contact():
	return config.render_template('contact.html')

if __name__ == '__main__':
	app.debug = True
	app.run()
