#!/usr/bin/python
# -*- coding: utf-8 -*-

 ## @package staben.py
# Dokumentation för denna modul.
#
# Innehåller alla 'routes' för hemsidan, t.ex. /prices eller /schedule.
# Innehåller även olika hjälpfunktioner.
#
# TODO
# Borde verkligen dela upp denna fil!

import os

# import Image
from PIL import Image
from werkzeug.utils import secure_filename

import config
#import model
from dev import db_commands, debug
# from dev import debug

# Used for new_password()
import string
import random
import time

app = config.app
render = config.render_template
request = config.request
url_for = config.url_for
session = config.session
flash = config.flash
redirect = config.redirect

debug = debug.debug
# async = decorators.async

static_texts = {'nollan': '<span class="nollanfont">nollan</span>', 'nollans': '<span class="nollanfont">nollans</span>', 'staben': '<span class="stabenfont">STABEN</span>'}

## Hämtar citat
#
# Hämtar alla citat som finns inlagda i databasen och returnerar ett random.
# 
# globals.update anropar en python-funktion så denna kan användas av Jinja.
# Se rad 114 i templates/template.html för anropet.
def get_quote():
	quotes = db_commands.get_quotes()
	if quotes:
		return quotes[random.randrange(len(quotes))].quote
	else:
		return False
config.app.jinja_env.globals.update(get_quote=get_quote)

## Hämtar en slumpad sträng
# 
#  @param length Anger vilken längd strängen ska ha. Förinställda värdet är att strängen blir 12 tecken långt.
# 
# Används för att skapa en slumpmässig sträng. Strängen kommer innehålla bokstäver och siffror.
# Används för att skapa lösenord.
def random_string(length=12):
	lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(length)]
	return ''.join(lst)

## Skickar e-mail
#
# @param recipients 			Anger vilken e-mailadress som ska ta emot e-mailet.
# @param subject				Anger titel  på e-mailet.
# @param email_body 			Anger innehållet i e-mailet i plaintext.
# @param html_body			Anger innehålleti e-mailet i html.
# 
# Skickar ett e-mail.
# OBS!
# Om det ska skickas asynkromt ska man använda send_async_email(msg) istället för config.mail.send(msg).
# Samt att man måste kommentera ut funktionen.
def send_email(recipients, subject, email_body=None, html_body=None):
	try:
		msg = config.Message(subject)
		msg.recipients = recipients
		if email_body:
			msg.body = email_body
		elif html_body:
			msg.html = html_body

		# send_async_email(msg)
		config.mail.send(msg)
		return True
	except:
		return False

## Asynkromt anrop för att skicka mail
# 
# @param msg Meddelandet som ska mailas.
# 
# Skickar mail asynkromt.
# OBS!
# Kan inte använda denna funktion när hemsidan ligger i CYD-poolen. Vet inte varför det inte fungerar.
# 
# @async
# def send_async_email(msg):
# 	config.mail.send(msg)

## Lägga till en session
# 
# @param db_user Innehåller all information om användaren från databasen.
# 
# Lägger till de sessioner som används på hemsidan.
def add_session(db_user):
	config.session['email'] = db_user['user'].email
	config.session['role'] = db_user['user'].role
	config.session['school_program'] = db_commands.get_user_school_program(db_user['user'].email)

	if db_user['info'].finished_profile:
		config.session['finished_profile'] = True
	else:
		config.session['finished_profile'] = False

	if db_user['info'].poll_done:
		config.session['poll_done'] = True
	else:
		config.session['poll_done'] = False

	return True

## Redigera ett sessionsvärde
# 
# Redigerar ett sessionsvärde till det man vill
# @param session_value Anger vilket sessionsvärde man vill ändra
# @param value Anger det nya värdet
def edit_session(session_value, value):
	config.session[session_value] = value

# Kan endast köras omm variabeln dev är satt som True.
# dev-variabeln finns i dev/host_option.py
# Denna BÖR sättas till False innan man laddar upp sidan!
if config.host_option.dev:
	## Route för att skapa databasen och alla tabeller
	# 
	# En route för att förenkla att skapa databasen. Binder ihop alla funktioner som skapar de olika tabellerna i databasen.
	# db_commands finns i dev/db_commands.py
	@app.route('/db_all')
	def db_all():
		try:
			db_commands.create_db()
			db_commands.create_school_programs()
			db_commands.create_school_classes()
			db_commands.create_contacts()
			db_commands.create_secret_code()
			db_commands.create_student_poll()
			db_commands.create_quotes()
			return 'SUUUUUUUUCCESS!!!!!'
		except:
			return 'NOOOOOO SUUUUUUUUCCESS!!!!!!!'

	## Skapar databasen
	# 
	# Skapar databasen. Denna måste köras innan alla andra funktioner som skapar tabeller!
	@app.route('/db_create')
	def db_create():
		return db_commands.create_db()

	## Tar bort databasen
	# 
	# OBS! Tar bort hela databasen.
	@app.route('/db_delete')
	def db_delete():
		return db_commands.delete_db()

	## Skapar sektionens program
	# 
	# Skapar de program som finns inom sektionen.
	@app.route('/db_programs')
	def db_programs():
		return db_commands.create_school_programs()

	## Skapar skolklasser
	# 
	# Skapar de skolklasser som finns inom de olika programmen.
	# db_programs() måste köras innan denna eftersom varje klass har en foreign key till det program det tillhör.
	@app.route('/db_classes')
	def db_classes():
		return db_commands.create_school_classes()

	## Skapar kontaktuppgifter
	# 
	# Skapar de olika kontaktuppgifter som nollorna ska lätt hitta.
	@app.route('/db_contacts')
	def db_contacts():
		return db_commands.create_contacts()
	
	## Skapar registreringskod
	# 
	# Skapar den registreringskod som är vald.
	@app.route('/db_code')
	def db_code():
		return db_commands.create_secret_code()

	## Skapar nolleenkäten
	# 
	# Skapar nolleenkäten.
	@app.route('/db_student_poll')
	def db_student_poll():
		return db_commands.create_student_poll()

## Route för index-sidan
@app.route('/')
def index():
	return render('index.html', session=session, bla=config.user_roles, st=static_texts)

## Route för pris-sidan
@app.route('/prices')
def prices():
	return render('prices.html', st=static_texts)

## Route för schema-sidan
# 
# Hämtar information från databasen.
@app.route('/schedule')
@app.route('/schedule/<show_week>')
def schedule(show_week=1):
	schedule = db_commands.get_schedule(show_week)
	return render('schedule.html', week=show_week, schedule=schedule)

## Route för galleri-sidan
# 
# @param album_id Specifierar vilket album som ska visas. Förinställda värdet är 0.
#
# Om album_id är 0 kommer alla gallerier visas, annars visas det valda galleriet.
@app.route('/gallery/album/<album_id>')
@app.route('/gallery/<notice>')
@app.route('/gallery')
def gallery(album_id=0):
	if album_id != 0:
		album = db_commands.get_a_album(album_id)
		uploader = db_commands.get_user_name(album.fk_user_id)
		photos = db_commands.get_all_pic_from_album(album_id)
		return render('gallery_album.html', album=album, photos=photos, album_id=album_id, uploader=uploader)
	albums = db_commands.get_all_albums(1)
	thumbnails = []
	uploaders = []
	if albums is not None:
		for a in albums:
			thumbnails.append(db_commands.get_thumbnail(a.id))
			uploaders.append(db_commands.get_user_name(a.fk_user_id))
	return render('gallery.html', albums=albums, thumbnails=thumbnails, uploaders=uploaders)

## Route för lägga upp galleri-sidan
# 
# @params album_id Anger vilket galleri som ska visas. Förinställda värdet är 0.
# 
# VET INTE RIKTIGT VAD DETTA ÄR TILL FÖR!
@app.route('/album_info/<album_id>', methods=['GET','POST'])
@app.route('/album_info', methods=['POST'])
def album_info(album_id=0):
	if album_id != 0:
		album = db_commands.get_a_album(album_id)
		pictures = db_commands.get_all_pic_from_album(album_id)
		return render('gallery_album_info.html',album_id=album_id, album=album, pictures=pictures, edit=True)
	#if album_id != 0 and request.method == 'POST':
	if request.method == 'POST':
		pic = request.form.getlist("picture_id")
		desc = request.form.getlist("description")
		for i,p in enumerate(pic):
			db_commands.update_picture(int(p), desc[i])
	notice = 1
	flash(u'Bra jobbat <span class="nollanfont">nollan</span>. Om det var ett nytt album du lade till så måste det godkännas av <span class="stabenfont">STABEN</span> innan det syns. Gjorde du en ändring av en eller flera beskrivningar så syns de direkt.')
	return redirect(url_for('gallery'))

## Route för ta bort galleri-sidan
@app.route('/delete_album/<album_id>')
def delete_alum(album_id):
	db_commands.delete_album(album_id)
	return redirect(url_for('gallery'))

# @app.route('/upload_pictures/<gallery_id>', methods=['GET', 'POST'])
# def upload_pictures(gallery_id):
# 	return 'hej'

## Route för ladda upp bilder-sidan
# 
# Laddar upp bilder. Se koden för kommentarer.
@app.route('/upload', methods=['GET','POST'])
def upload():
	# Hämtar den inloggade användarens information
	user = db_commands.get_db_user(db_user_email=session['email'])

	# Uppladdningsformuläret skickas som POST
	# Om sidan kallas på med GET kommer uppladdningsforumläret visas
	if request.method == 'POST':
		# Alla bilder
		photos = request.files.getlist('file[]')

		# Sätter de olika värdena för galleriet
		title = request.form['title']
		description = request.form['description']
		uploader = request.form['uploader']
		date = request.form['date']

		#Haha visa ej för nollan, ju
		time = '13:37:00'

		# Spara galleriet i databasen och returnera det ID galleriet fick
		album_id_int = db_commands.save_album(uploader, date, time, title, description, 0)
		album_id = 'album_' + str(album_id_int)
	
		photo_paths = []
		photo_ids = []

		# Sätt rätt mapp för bilderna
		album_path = config.host_option.upload_dir + 'gallery/' + album_id + '/'
		p_thumb_path = album_path + 'thumbnail/'

		# Om mapparna inte finns skapas de
		if not os.path.exists(album_path):
			os.makedirs(album_path)
		if not os.path.exists(p_thumb_path):
			os.makedirs(p_thumb_path)

		# Sätt provbildens storlek
		thumbnail_size = 200, 200

		# Gå igenom alla bilder som har laddats upp
		for p in photos:
			path_to_file = album_path + secure_filename(p.filename)
			photo_paths.append(secure_filename(p.filename))

			p.save(path_to_file)
			
			p_thumb = Image.open(path_to_file)
			p_thumb.save(path_to_file)
			p_thumb.thumbnail(thumbnail_size, Image.ANTIALIAS)
			p_thumb.save(p_thumb_path + p.filename)
		
			p_id = db_commands.save_picture(uploader, album_id_int, date, time, secure_filename(p.filename), 'Beskrivning')
			photo_ids.append(p_id)
		return render('gallery_album_info.html', photo_ids=photo_ids, photo_paths=photo_paths,album_id=album_id)
	return render('upload.html',user=user)

## Route för ladda upp blogg-sidan
# 
# @param blog_id Anger vilken blogg som ska visas. Förinställda värdet är None.
# 
# Om blog_id inte är None kommer den valda blogga hämtas från databasen.
# Annars visas alla inlägg.
@app.route('/blog')
@app.route('/blog/<blog_id>')
def blog(blog_id=None):
	if not blog_id is None:
		db_blog = db_commands.get_blog(b_id=blog_id)
		gallery = db_commands.get_a_album(db_blog[0].fk_gallery_album_id)
		photos = db_commands.get_all_pic_from_album(db_blog[0].fk_gallery_album_id)
		comments = db_commands.get_comments(blog_id)
	else:
		gallery = None
		photos = None
		comments = None
	return render('blog.html', blogs=db_blog, blog_id=blog_id, gallery=gallery, photos=photos)

## Route för kontakt-sidan
# 
# @param show_page Anger vilken kontaktsida som ska visas. Förinställda värdet är att den ska visa kontaktsidan.
@app.route('/contact')
@app.route('/contact/<show_page>')
def contact(show_page='contact'):
	role_klass = 0
	role_studie = 1
	klassforestandare = db_commands.get_contacts(role_klass)
	studievagledning = db_commands.get_contacts(role_studie)
	return render('contact.html', show=show_page, klassforestandare=klassforestandare, studievagledning=studievagledning, st=static_texts)

## Route för login-sidan
@app.route('/user/login', methods=['POST'])
def login():
	if request.form['email'] not in session:
		if request.method == 'POST':
			user = db_commands.get_db_user(db_user_email=request.form['email'], db_user_password=request.form['password'])

			if user:
				# user_info['user'] contains email, password and role (from the table users)
				# user_info['info'] contains all the user's information (from the table userInformation)
				if add_session(user):
					db_commands.add_login_count(request.form['email'])

					if not session['poll_done']:
						redirect_to = 'profile_student_poll'
					else:
						redirect_to = 'profile_edit'

					return redirect(url_for(redirect_to, user_email=request.form['email']))
				else:
					return 'Ojoj, detta var ju inte korrekt!'
			else:
				return render('login.html', login=False)
		else:
			return redirect(url_for('profile_class', user_email=request.form['email']))
	return render('login.html', login=False)

## Route för logga ut-sidan
@app.route('/user/signout')
def signout():
	session.clear()
	return redirect(url_for('index'))

## Route för register-sidan
# 
# Kollar igenom varje värde som måste vara satt.
# Om värdet inte är satt kommer användaren bli skickad tillbaka till register-sidan.
@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		if not db_commands.check_if_email_exist(request.form['email']):
			forbidden_chars = [u'å', u'ä', u'ö']
			forbidden_chars_email = [x for x in forbidden_chars if x in request.form['email']]

			if len(forbidden_chars_email) == 0:
				if request.form['email'] != '':
					if str(request.form['regCode']) == str(db_commands.get_register_code().code):
						debug('register', 'email och code funkar')
						if request.form['password'] == request.form['rep_password']:
							debug('register', 'Passwords are the same')
							if db_commands.register_user(request.form):
								user = db_commands.get_db_user(db_user_email=request.form['email'], db_user_password=request.form['password'])['user']

								if user:
									if db_commands.add_user_information(user.id):
										debug('register', 'Registration succeeded')
										user = db_commands.get_db_user(user_id=user.id)
										add_session(user)
										return redirect(url_for('profile_edit', user_email=user['user'].email))
									else:
										debug('register', 'Error, could not add user information')
										return redirect(url_for('register'))
								else:
									debug('register', 'Error, could not get user')
									return redirect(url_for('register'))
							else:
								debug('register', 'Error, could not register user')
								return redirect(url_for('register'))
						else:
							debug('register', 'Error, the password did not match')
							flash(u'Du måste ange samma lösenord i båda rutorna.')
							return redirect(url_for('register'))
					else:
						debug('register', 'Error, the user did not type the correct register code')
						flash(u'Du angav fel registreringskod! Denna kod ska du ha fått hem till din bokföringsadress i brevet från <span class="stabenfont">Generalen</span>')
						return redirect(url_for('register'))
				else:
					debug('register', 'Error, the user did not type his email')
					flash(u'Du måste ange din e-mail!')
					return redirect(url_for('register'))
			else:
				debug('register', 'Error, the user typed a forbidden character as his e-mail')
				flash(u'Din e-post får inte innehålla å, ä eller ö!')
				return redirect(url_for('register'))
		else:
			debug('register', 'Error, the email already exists')
			flash(u'E-posten du angav är redan registrerad!')
			return redirect(url_for('register'))
	else:
		return render('register.html')

## Route för glömt lösenord-sidan
# 
# @param code Om en användare har frågat efter nytt lösenord och fått en kod kommerr code bli satt. Förinställda värdet är None.
@app.route('/forgot_password', defaults={'code': ''}, methods=['POST', 'GET'])
@app.route('/forgot_password/<code>', methods=['POST', 'GET'])
def forgot_password(code=None):
	if code:
		# Query with the correct e-mail as well
		# This can be done when the function is fixed to be more general!
		recover_user = db_commands.get_db_user(recover_code=code)

		if recover_user:
			new_password = random_string()
			new_password_bcrypt = config.bcrypt.generate_password_hash(new_password)
			recover_code_md = config.MultiDict([('recover_code', '')])
			if db_commands.update_db_user(recover_user.email, recover_code_md):
				password_dict = {'new_password': new_password, 'repeat_password': new_password, 'current_password': recover_user.password}
				if db_commands.update_db_pw_from_code(recover_user.email, password_dict):
					body = '''<b>Hej igen nollan!</b>
					<br />
					Ditt nya lösenord är: %s
					<br />
					Se till att bevara detta väl, men kom ihåg, STABEN ser allt!
					''' % (new_password)
					if send_email([recover_user.email], 'Ditt nya lösenord på staben.info', html_body=body):
						flash(u'Ditt nya lösenord har blivit skickat till din e-post.')
						return redirect(url_for('index'))
					else:
						debug('forgot_password', 'Error, could not send the recovery e-mail')
						return render('forgot_password.html')
				else:
					debug('forgot_password', 'Error, could not update password')
					return render('forgot_password.html')
			else:
				debug('forgot_password', 'Error, could not update user')
				return render('forgot_password.html')
		else:
			flash(u'Återställningskoden finns ej.')
			return render('forgot_password.html')

	elif request.method == 'POST':
		if db_commands.check_if_email_exist(request.form['email']):
			if request.form['email'] != '':
				# Send en e-mail to request.form['email'] with an url that will reset the user's password
				recover_code = random_string(25)
				body = '''<b>Hej nollan!</b>
					<br />
					Tryck <a href='http://www.staben.info/forgot_password/%s' target='_blank'>här</a> för att få nytt lösenord på www.staben.info
					<br /><br />
					<b>OBS! Om du ej har förfrågat att få ditt lösenord återställt kan du bortse från detta e-brev!</b>
					''' % (recover_code)
				if send_email([request.form['email']], 'Glömt lösenord på staben.info', html_body=body):
					recover_code_md = config.MultiDict([('recover_code', recover_code)])
					db_commands.update_db_user(request.form['email'], recover_code_md)

					flash(u'Ett e-post har blivit skickad till %s med en återställningslänk som du måste följa för att återställa ditt lösenord.' % (request.form['email']))
					return render('forgot_password.html')
			else:
				flash(u'Du måste ange en e-post.')
				return render('forgot_password.html')
		else:
			flash(u'Den angivna e-posten finns inte i databasen.')
			return render('forgot_password.html')
	else:
		return render('forgot_password.html')

## Route för nollebricke-sidan
@app.route('/student_badge')
def student_badge():
	return render('student_badge.html')

## Route för nollehandbok-sidan
@app.route('/student_book')
def student_book():
	return render('student_book.html')

## Användarprofil

## Route för användares profil-sidan
# 
# @param user_email Kommer vara användarens e-mail som hen registrerade sig med.
@app.route('/profile/<user_email>/edit/')
def profile_edit(user_email):
	if session and user_email == session['email']:
		user = db_commands.get_db_user(db_user_email=session['email'])
		school_programs = db_commands.get_school_programs()
		db_selection = str(user['info'].school_class) + '|' + str(user['info'].school_program)

		return render('profile_edit.html', \
			user=user['user'], \
			user_info=user['info'], \
			school_programs=school_programs,
			school_classes=db_commands.get_school_classes(), \
			st=static_texts, \
			db_selection=db_selection)
	else:
		return render('login.html', login=False)

## Route för spara profil-sidan
# 
# @param user_email Kommer vara användarens e-mail som hen registrerade sig med.
@app.route('/profile/<user_email>/save/', methods=['POST'])
def profile_save(user_email):
	if session and user_email == session['email']:
		if request.form['firstname'] != '' and request.form['lastname'] != '':
			copy_request_form = request.form.copy()
			copy_request_form.add('phonenumber_vis', 1 if 'phonenumber_vis' in request.form else 0)
			copy_request_form.add('finished_profile', 1)
			db_commands.update_db_user(user_email, copy_request_form)

			if session['finished_profile'] and not session['poll_done']:
				redirect_to = 'profile_student_poll'
			elif session['finished_profile']:
				redirect_to = 'profile_edit'
			else:
				redirect_to = 'profile_student_poll'

			edit_session('finished_profile', True)
			edit_session('school_program', db_commands.get_user_school_program(user_email))
			return redirect(url_for(redirect_to, user_email=user_email))
		else:
			return redirect(url_for('profile_edit', user_email=user_email))
	else:
		return render('login.html', login=False)

## Route för spara lösenord-sidan
# 
# @param user_email Kommer vara användarens e-mail som hen registrerade sig med.
@app.route('/profile/<user_email>/save/password', methods=['POST'])
def profile_save_password(user_email):
	if session and user_email == session['email']:
		if db_commands.update_db_pw(user_email, request.form):
			return redirect(url_for('index', user_email=user_email))
		else:
			return "Not updated"
	else:
		return render('login.html', login=False)

## Route för skolprogram-sidan
# 
# @param user_email Kommer vara användarens e-mail som hen registrerade sig med.
# @param school_program Anger vilket skolprogram användaren vill kolla på.
@app.route('/profile/<user_email>/class/<school_program>')
def profile_class(user_email, school_program):
	if session and user_email == session['email']:
		program_users = db_commands.get_school_program_users(school_program)
		# Set school_program to D if the user has not updated his profile
		return render('profile_class.html', \
			user_school_program=session['school_program'], \
			chosen_school_program=school_program if school_program != str(0) else 'D', \
			program_users=program_users)
	else:
		return render('login.html', login=False)

## Route för nolleenkät-sidan
# 
# @param user_email Kommer vara användarens e-mail som hen registrerade sig med.
@app.route('/profile/<user_email>/student_poll/')
def profile_student_poll(user_email):
	if session and user_email == session['email']:
		user = db_commands.get_db_user(db_user_email=session['email'])

		student_poll_user_answers = config.MultiDict([])
		for index, value in enumerate(db_commands.get_student_poll_answers(user_email)):
			student_poll_user_answers.add(int(value), index)

		return render('profile_student_poll.html', \
			student_poll_prefixes=db_commands.get_student_poll_prefix(), \
			student_poll_questions=db_commands.get_student_poll_question(), \
			user_poll_done=user['info'].poll_done, \
			student_poll_user_answers=student_poll_user_answers, \
			st=static_texts)
	else:
		return render('login.html', login=False)

## Route för spara nolleenkät-sidan
# 
# @param user_email Kommer vara användarens e-mail som hen registrerade sig med
@app.route('/profile/<user_email>/save/student_poll/', methods=['POST'])
def profile_save_student_poll(user_email):
	if session and user_email == session['email']:
		# Check if the user already have done the student poll
		# Added this check so that no body tries to save his/hers poll more than once
		if db_commands.get_db_user(db_user_email=session['email'])['info'].poll_done == 0:
			if db_commands.update_db_user(user_email, config.ImmutableMultiDict([('poll_done', u'1')])):
				if db_commands.save_student_poll(user_email, request.form):
					edit_session('poll_done', True)
					return redirect(url_for('profile_student_poll', user_email=user_email))
				else:
					debug('profile_save_student_poll', 'Could not save the student poll')
					return redirect(url_for('profile_student_poll', user_email=user_email))
			else:
				debug('profile_save_student_poll', 'Could not update poll_done on user')
				return redirect(url_for('profile_student_poll', user_email=user_email))
		else:
			return redirect(url_for('profile_student_poll'))
	else:
		return render('login.html', login=False)

## Route för lägga till blogg-sidan
# 
# @param user_email Kommer vara användarens e-mail som hen registrerade sig med.
@app.route('/profile/<user_email>/blog')
def profile_blog(user_email):
	if session and user_email == session['email'] and (session['role'] is 6 or session['role'] is 0):
		blog = db_commands.check_if_blog_done(time.strftime('%Y-%m-%d', time.localtime()))
		if blog is None:
			return render('profile_blog.html', gallery=db_commands.get_gallery(), blog=None)
		else:
			return render('profile_blog.html', gallery=db_commands.get_gallery(), blog=blog)
	else:
		return render('admin_fail.html')

## Route för lägga till eller redigera blogg-sidan
# 
# @param user_email Kommer vara användarens e-mail som hen registrerade sig med.
# @param command Anger vilket kommando som ska användas. Kan vara antigen add eller edit.
@app.route('/profile/<user_email>/blog/<command>', methods=['POST'])
def profile_blog_entry(user_email, command):
	if session and user_email == session['email'] and (session['role'] is 6 or session['role'] is 0):
		copy_request_form = request.form.copy()
		localtime = time.localtime()
		current_date = time.strftime('%Y-%m-%d', localtime)
		current_time = time.strftime('%H:%M', localtime)
		copy_request_form.add('date', current_date)
		copy_request_form.add('time', current_time)
		copy_request_form.add('fk_user_id', int(db_commands.get_db_user(db_user_email=user_email)['user'].id))

		if command == 'add':
			if db_commands.save_blog(copy_request_form):
				return redirect(url_for('blog'))
			else:
				return 'Kunde inte adda blogginlägget!'
		elif command == 'edit':
			if db_commands.save_blog(copy_request_form, db_commands.get_blog(b_date=current_date).id):
				return redirect(url_for('blog'))
			else:
				return 'Kunde inte uppdatera blogginlägget!'
		else:
			return 'Felaktigt kommando!'
	else:
		return render('admin_fail.html')

## Adminverktyg

## Route för random verktyg-sidan
# 
# Här läggs lite random verktyg som förenklar arbetet lite.
@app.route('/admin/pages/')
def admin_pages():
	# Need to check that the user is signed in and is an admin
	if db_commands.check_role(session['email']) == 0:
		return render('admin_pages.html')
	else:
		return render('admin_fail.html')

## Route för spara random verktyg-sidan
# 
# @param command Anger vad man vill göra. Nu finns bara quote som lägger till ett citat.
@app.route('/admin/pages/save/<command>', methods=['GET', 'POST'])
def admin_page_save(command):
	if db_commands.check_role(session['email']) == 0:
		if request.method == 'POST':
			if command == 'quote':
				flash(u'Citat inlagt.')
				result = db_commands.admin_add_quote(request.form)

			if result:
				return redirect(url_for('admin_pages'))
			else:
				return 'Couldn\'t add quote'
	else:
		return render('admin_fail.html')

## Route för lägga till kontakt-sidan
@app.route('/admin/addcontact/', methods=['GET', 'POST'])
def admin_addcontact():
	if db_commands.check_role(session['email']) is 0:
		if request.method == 'POST':
			result = db_commands.add_contact(request.form['name'], request.form['phonenumber'],
											 request.form['email'],request.form['role'],
											 request.form['school_class'], request.form['studie_link'])
			return render('admin_addcontact.html', result=result)
		elif request.method == 'GET':
			return render('admin_addcontact.html')
	else:
		return render('admin_fail.html')

## Route för visa användare-sidan
@app.route('/admin/users/')
def admin_get_all_users():
	# Need to check that the user is signed in and is an admin
	if db_commands.check_role(session['email']) is 0:
		users = db_commands.admin_get_all_users()
		return render('admin_get_all_users.html', users=users)
	else:
		return render('admin_fail.html')

## Route för nolleenkätsinställnings-sidan
# 
# Kan lägga till prefix, frågor.
# Kan ändra hur många nollor det ska vara i varje grupp.
# Kan lägga till alla nollor i sin rätta grupp. OBS! Detta fungerar INTE! Måste skriva om hela nolleenkätssaken. GLHFosv.
@app.route('/admin/student_poll/')
def admin_student_poll():
	if db_commands.check_role(session['email']) is 0:
		return render('admin_student_poll.html', \
			prefixes=db_commands.get_student_poll_prefix(), \
			dialects=db_commands.get_student_poll_dialects())
	else:
		return render('admin_fail.html')

## Route för spara nolleenkätsinställningar-sidan
#
# @param command Anger vilket kommando som ska användas. Kan vara prefix, question eller max_students.
@app.route('/admin/student_poll/save/<command>', methods=['POST'])
def admin_student_poll_save(command):
	if db_commands.check_role(session['email']) is 0:
		if request.method == 'POST':
			if command == 'prefix':
				flash('Prefix inlagt.')
				result = db_commands.add_student_poll_prefix(request.form)
			elif command == 'question':
				flash(u'Fråga inlagd.')
				result = db_commands.add_student_poll_question(request.form)
			elif command == 'max_students':
				flash(u'Max antal studenter inlagt.')
				result = db_commands.add_student_poll_max_students(request.form)

			if result:
				# Perhaps add some kind of alert here to show that the
				#  prefix/question was successfully added??
				return redirect(url_for('admin_student_poll'))
			else:
				return 'Couldn\'t add to poll'
	else:
		return render('admin_fail.html')

## Route för se alla nolleenkäter-sidan
# 
# Denna är väldigt seg, mycket för att nolleenkäten är så otroligt stor och därmed är databasen väldigt stor så det tar tid att sammanställa allting.
@app.route('/admin_student_poll_result')
def admin_student_poll_result():
	if db_commands.check_role(session['email']) is 0:
		return render('admin_student_poll_result.html', \
			users_info=db_commands.admin_get_all_users_w_poll_done(), \
			dialects=db_commands.get_student_poll_dialects(), \
			user_w_points=db_commands.admin_get_top_three_groups())
	else:
		return render('admin_fail.html')

## Route för visa  en students nolleenkät-sidan
#
# @param user_id Anger vilken students nolleenkät man vill se.
@app.route('/admin_show_student_poll_result/<user_id>')
def admin_show_student_poll_result(user_id):
	if db_commands.check_role(session['email']) is 0:
		alot_of_info = db_commands.admin_get_user_poll_answer(user_id)
		return render('admin_student_poll_user_result.html', \
			user=alot_of_info[1], \
			alot_of_info=alot_of_info[2], \
			dialects=db_commands.get_student_poll_dialects(), \
			number_of_dialects=len(db_commands.get_student_poll_dialects()), \
			user_points=db_commands.admin_calc_user_points(user_id))
	else:
		return render('admin_fail.html')

## Route för att lägga till en användare-sidan
# 
# Inte riktigt säker på vad denna skulle göra.
@app.route('/admin_insert_user_to_group', methods=['POST'])
def admin_insert_user_to_group():
	if db_commands.check_role(session['email']) is 0:
		if request.method == 'POST':
			print db_commands.admin_insert_user_to_group()
			
			# REPLACE THE FINISHED MD WITH THIS::::::
			# users = db_commands.admin_get_all_users()
			# return render('admin_student_poll_show_assigned_groups.html', \
			# 	md=db_commands.admin_insert_user_to_group(), \
			# 	users=users, \
			# 	dialects=db_commands.get_student_poll_dialects(), \
			# 	school_programs=db_commands.get_school_programs())
	else:
		return render('admin_fail.html')

## Route för att redigera en nollans svar-sidan
# 
# Denna används till nolleintervjuerna där de som intervjuar kan dubbelkolla allting som nollan har angett i sin profil.
# Här ställer även den som intervjuar frågor om nollan vill tillhöra en speciell grupp.
# OBS! Denna fungerar inte som den ska (tror jag) och bör kollas över.
@app.route('/admin_edit_user/<user_id>')
def admin_edit_user(user_id):
	if db_commands.check_role(session['email']) is 0:
		return render('admin_edit_user.html', user=db_commands.get_db_user(user_id=user_id))
	else:
		return render('admin_fail.html')

## Route för att spara en nollans svar-sidan
# 
# @param user_id Anger vilken nollans svar man ska spara.
# 
# 110, 111, 112 och 113 är kollen om nollan vill tillhöra någon speciell grupp eller inte.
# Om nollan vill det kommer hen få extra poäng på de grupperna som kollen tillhör.
@app.route('/admin_edit_user/save/<user_id>', methods=['POST'])
def admin_edit_user_save(user_id):
	if db_commands.check_role(session['email']) is 0:
		try:
			copy_request_form = request.form.copy()

			# Need this check because if the checkbox is checked it won't give it a value
			# so it removes the value from the dict and re-adds it with value 1
			if 'bicycle' in request.form:
				copy_request_form.pop('bicycle')
				copy_request_form.add('bicycle', 1)

			if '110' in request.form:
				db_commands.save_student_poll(request.form['email'], config.ImmutableMultiDict([('110', 110)]))
			if '111' in request.form:
				db_commands.save_student_poll(request.form['email'], config.ImmutableMultiDict([('111', 111)]))
			if '112' in request.form:
				db_commands.save_student_poll(request.form['email'], config.ImmutableMultiDict([('112', 112)]))
			if '113' in request.form:
				db_commands.save_student_poll(request.form['email'], config.ImmutableMultiDict([('113', 113)]))
			copy_request_form.pop('email')
			db_commands.update_db_user(request.form['email'], copy_request_form)

			return redirect(url_for('admin_get_all_users'))
		except:
			return False
	else:
		return render('admin_fail.html')

## Route för visa en nollan-sidan
# 
# @param user_id Anger vilken nollan man vill kolla på.
@app.route('/admin_show_user/<user_id>')
def admin_show_user(user_id):
	if db_commands.check_role(session['email']) is 0:
		return render('admin_show_user.html', \
			user=db_commands.get_db_user(user_id=user_id), \
			user_points=db_commands.admin_calc_user_points(user_id=user_id, order=True), \
			dialects=db_commands.get_student_poll_dialects())
	else:
		return render('admin_fail.html')

## Route för godkänna galleri-sidan
# 
# @param album_id Anger vilket galleri man vill kolla på. Förinställda värdet är 0.
# 
# Om album_id inte är 0 kommer den visa det galleri man vill se.
# Om man godkänner galleriet kommer formuläret skicka en POST request och då godkänns galleriet.
@app.route('/admin_approve_album/<album_id>', methods=['GET','POST'])
@app.route('/admin_approve_album', methods=['GET','POST'])
def admin_approve_album(album_id=0):
	if album_id != 0:
		album = db_commands.get_a_album(album_id)
		uploader = db_commands.get_user_name(album.fk_user_id)
		photos = db_commands.get_all_pic_from_album(album_id)
		return render('gallery_album.html', album=album, photos=photos, album_id=album_id, uploader=uploader, admin_approve=True)
	if request.method == 'POST':
		album_id = request.form['album_id']
		db_commands.album_approve(album_id)
		return redirect(url_for('gallery'))
	albums = db_commands.get_all_albums(0)
	thumbnails = []
	uploaders = []
	if albums is not None:
		for a in albums:
			thumbnails.append(db_commands.get_thumbnail(a.id))
			uploaders.append(db_commands.get_user_name(a.fk_user_id))
	return render('gallery.html', albums=albums, thumbnails=thumbnails, uploaders=uploaders, admin_approve=True)

## Route för lägga till en kommentar-sidan
# 
# @param blog_id Anger vilken blogg man vill lägga till kommentaren i.
@app.route('/add_comment/<blog_id>', methods=['GET','POST'])
def add_comment(blog_id):
	copy_request_form = request.form.copy()

	localtime = time.localtime()
	current_date = time.strftime('%Y-%m-%d', localtime)
	current_time = time.strftime('%H:%M', localtime)
	copy_request_form.add('date', current_date)
	copy_request_form.add('time', current_time)
	copy_request_form.add('fk_user_id', int(db_commands.get_db_user(db_user_email=session['email'])['user'].id))
	copy_request_form.add('fk_blog_id', int(blog_id))

	return blog_id

## Route för ansöka till STABEN-sidan
@app.route('/nystaben')
def nystaben():
	return render('nystaben.html', st=static_texts);

# Does not work..
# @app.errorhandler(403)
# def page_not_found(e):
#     return render('error.html', st=static_texts), 403
# @app.errorhandler(404)
# def page_not_found(e):
#     return render('error.html', st=static_texts), 404
# @app.errorhandler(410)
# def page_not_found(e):
#     return render('error.html', st=static_texts), 410
# @app.errorhandler(500)
# def page_not_found(e):
#     return render('error.html', st=static_texts), 500

## Funktion för att rensa allt från hemsidan som inte ska vara kvar efter nedstängning.
@app.teardown_appcontext
def shutdown_session(exception=None):
	config.db_session.remove()

## Från flask manuallen:
# The if __name__ == '__main__': makes sure the server only runs if the script is executed directly from the Python interpreter and not used as an imported module.
if __name__ == '__main__':
	app.run(host=config.host_option.HOST, debug=config.host_option.DEBUG)
