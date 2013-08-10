import os

local = True

if local:
	dbhost = '127.0.0.1'
	dbuser = 'STABEN'
	dbpass = 'generalhenrik'
	dbname = 'STABEN'
	student_poll_file = os.getcwd() + '/dev/files/studentpoll.csv'
	quote_file = os.getcwd() + '/dev/files/quotes.txt'
else:
	dbhost = '127.0.0.1'
	dbuser = 'dstaben'
	dbpass = 'cjnW5A82YhcBWAcK'
	dbname = 'dstaben'
	student_poll_file = '/www/dstaben/htdocs/dev/files/studentpoll.csv'
	quote_file = '/www/dstaben/htdocs/dev/files/quotes.txt'