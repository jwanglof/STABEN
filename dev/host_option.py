import os

local = True
dev = True

if local:
	dbhost = '0.0.0.0'
	dbuser = 'STABEN'
	dbpass = 'generalhenrik'
	dbname = 'STABEN'
	root_path = os.getcwd()
	DEBUG = True
else:
	dbhost = '127.0.0.1'
	dbuser = 'dstaben'
	dbpass = 'cjnW5A82YhcBWAcK'
	dbname = 'dstaben'
	root_path = '/www/dstaben/htdocs'
	DEBUG = False

student_poll_file = root_path + '/dev/files/studentpoll.csv'
quote_file = root_path + '/dev/files/quotes.txt'