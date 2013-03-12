import config
#import model
from dev import db_commands

app = config.app

# DEV OPTIONS
# NEEDS TO BE REMOVED IN PRODUCTION MODE
@app.route('/db_create')
def db_create():
	return db_commands.create_app()

@app.route('/')
def index():
	return config.render_template('index.html')

@app.route('/schedule')
def schedule():
	return config.render_template('schedule.html')

@app.route('/student_poll')
def student_poll():
	return config.render_template('student_poll.html')

@app.route('/gallery')
def gallery():
	return config.render_template('gallery.html')

@app.route('/blog')
def blog():
	return config.render_template('blog.html')

@app.route('/contact')
def contact():
	return config.render_template('contact.html')

if __name__ == '__main__':
	app.debug = True
	app.run()
