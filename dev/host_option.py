import os

local = True

if local:
	dbuser = 'STABEN'
	dbpass = 'generalhenrik'
	dbname = 'STABEN'
	student_poll_file = os.getcwd() + '/dev/files/studentpoll.csv'
	quote_file = os.getcwd() + '/dev/files/quotes.txt'
else:
	dbuser = 'dstaben'
	dbpass = 'cjnW5A82YhcBWAcK'
	dbname = 'dstaben'
	student_poll_file = '/www/dstaben/htdocs/dev/files/studentpoll.csv'
	quote_file = '/www/dstaben/htdocs/dev/files/quotes.txt'