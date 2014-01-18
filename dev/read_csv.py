import csv

## Read student poll csv file
#
# Reads a CSV file with all the prefixes, questions, dialects and max students for the student poll
#
# Run example
# - Make sure that dev/studentpoll.csv is up to date!
#
# - studentPollCsv = ReadStudentPollCsvFile('studentpoll.csv')
# - print studentPollCsv.get_prefixes()
#  + {1: 'Har med sig', 2: 'Gillar', ....}
# - print studentPollCsv.get_questions()
#  + {1: ['dattamaskin', 'blabla', 'bla'], 2: ['dddd', 'ddd'], ....}
# - print studentPollCsv.get_dialects()
#  + {1: 'Idolbok', 2: 'MacGyver', ....}
# - print studentPollCsv.get_points()
#  + {1: ['dattamaskin', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '', '', '', '1', '', '', '', '', '', '', '2', ''], ....}
# - print studentPollCsv.get_max_students()
#  + {1: '8', 2: '8', ....}
# 
# After that just run /db_all (or just /db_student_poll for just the student poll DB entries)
# 
# @author 	Johan Wänglöf
# @date	2013-07 - 2013-08
# @version 	1
class ReadStudentPollCsvFile():
	## The constructor
	# 
	# @param filename Set from which file to read from
	def __init__(self, filename):
		csv.register_dialect('commas', delimiter=',')
		self.filename = filename

	## Check for illegal chars
	# 
	# @param row Specifies which row that needs to be checked
	# 
	# Check so that row doesn't contain any 'illegal' characters
	# Just add the illegal chars from the document on the row
	#
	# This can probably be more optimized!
	def check(self, row):
		if row[:1] == ',' or row == 'SUmma' or row == 'Summa' or row == '' or row == 'Summa':
			return False
		else:
			return True

	## Get prefixes
	# 
	# Get all the prefixes from the file
	# 
	# Examples:
	# Har med sig, Gillar, Bekväm med etc
	# 
	# Rules:
	# The prefix MUST begin with an uppercase. This is needed so the script can see if it is a prefix or a question
	def get_prefixes(self):
		i = 1
		prefixes = {}

		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if self.check(row[0]) and row[0][:1].isupper():
					prefixes[i] = row[0]
					i += 1
		return prefixes

	## Get questions
	# 
	# Get all questions from the file
	# 
	# Examples:
	# dattamaskin, verktygslåda, målargrejor etc
	def get_questions(self):
		# i will determine which dialect id the question belongs to
		# question_list contains all the questions
		# questions contains dialect id with question_list
		i = 0
		question_list = []
		questions = {}

		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if self.check(row[0]) and row[0][:1].isupper():
					if i > 0:
						questions[i] = question_list
						question_list = []
					i += 1

				# Replace each staben with the correct font
				if self.check(row[0]) and row[0][:1].islower():
					question_list.append(row[0].replace('staben', '<span class=\'stabenfont\'>STABEN</span>'))

		# Need this so the last list is added to questions!
		questions[i] = question_list
		return questions

	## Get dialects
	# 
	# Get all the dialects from the file
	# Dialects are the different groups
	# 
	# Examples:
	# Idolbok,MacGyver,Mission Impossible
	def get_dialects(self):
		dialects = {}
		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile, dialect='commas')
			dialect_list = [x for x in reader][0][1:]

		for index, x in enumerate(dialect_list):
			dialects[index+1] = x
		return dialects

	## Get points
	# 
	# Get the points for each question
	# This can probably be re-written to be more optimized!
	def get_points(self):
		point_list = []
		points = {}
		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile, dialect='commas')
			for row in reader:
				if self.check(row[0]) and row[0][:1].islower():
					point_list.append(row)

		questions = [y for x in self.get_questions().values() for y in x]
		for i, q in enumerate(questions):
			# print 'Question: ' + point_list[i][0]
			# print 'Points: ', point_list[i][1:]
			# points[i+1] = point_list[i]
			points[i+1] = {point_list[i][0]: point_list[i][1:]}
		return points

	## Get max students
	# 
	# Get the maximum amount of students that are allowed to be in a group
	# Is placed at the bottom of the file
	#
	# Rules:
	# The line needs to start with max_students (or something similar) because this text is removed
	def get_max_students(self):
		max_students_w_dialect = {}

		with open(self.filename, 'rb') as csvfile:
			## [-1] = Take the last column in the file
			## [1:] = Remove the first element (which in this case is max_students)
			reader = csv.reader(csvfile, dialect='commas')
			max_student_list = [y for y in reader][-1][1:]

		for d_id, dialect in (self.get_dialects()).iteritems():
			max_students_w_dialect[d_id] = max_student_list[d_id-1]

		return max_students_w_dialect