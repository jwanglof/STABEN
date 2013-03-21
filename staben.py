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

@app.route('/')
def index():
	return render('index.html')

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
			if (db_commands.get_db_user(get_form.form['email'],get_form.form['password']) == "TRUE"):
				return render('profile.html', user_email=config.session['email'])
	else:
		return render('profile.html', user_email=config.session['email'])
	return render('login.html', login=False)

@app.route('/user/profile')
def profile():
	user_info = db_commands.get_db_user(config.session['email'])
	#print user_info.email
	return render('profile.html', user_info=user_info)

@app.route('/user/signout')
def signout():
	config.session.clear()
	return config.redirect(url_for('index'))


if __name__ == '__main__':
	app.debug = True
	app.run()
