import os

local = True

if local:
	dbuser = 'STABEN'
	dbpass = 'generalhenrik'
	dbname = 'STABEN'
	student_poll_file = os.getcwd() + '/dev/studentpoll.csv'
else:
	dbuser = 'dstaben'
	dbpass = 'cjnW5A82YhcBWAcK'
	dbname = 'dstaben'
	student_poll_file = '/www/dstaben/htdocs/dev/studentpoll.csv'