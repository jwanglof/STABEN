import os

# True will set the variables to match the local computer
# False will set them to CYD-poolens settings
local = True

# True will give access to the database creation routers
# False will deny access to these
dev = True

if local:
	dbhost = '127.0.0.1'
	dbuser = 'STABEN'
	dbpass = 'generalhenrik'
	dbname = 'STABEN'
	root_path = os.getcwd()
	DEBUG = True
	HOST = '127.0.0.1'
else:
	dbhost = '127.0.0.1'
	dbuser = 'dstaben'
	dbpass = 'cjnW5A82YhcBWAcK'
	dbname = 'dstaben'
	root_path = '/www/dstaben/htdocs'
	DEBUG = False
	HOST = '0.0.0.0'

# Set directory paths
student_poll_file = root_path + '/dev/files/studentpoll.csv'
quote_file = root_path + '/dev/files/quotes.txt'
upload_dir = root_path + '/static/upload/'