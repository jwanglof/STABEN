import csv

###
# Need to add the questions to a list
# since dict's aren't ordered
###

###
# Run example:
# - FIRST!
# -- Make sure that dev/studentpoll.csv is up to date
# 
# After that just run /db_all (or just /db_student_poll for just the student poll DB entries)
###
class ReadStudentPollCsvFile():
	def __init__(self, filename):
		csv.register_dialect('commas', delimiter=',')
		self.filename = filename

	# Check so that row doesn't contain any 'illegal' characters
	def check(self, row):
		if row[:1] == ',' or row == 'SUmma' or row == 'Summa' or row == '':
			return False
		else:
			return True

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

				if self.check(row[0]) and row[0][:1].islower():
					question_list.append(row[0].replace('staben', '<span class=\'stabenfont\'>STABEN</span>'))

		# Need this so the last list is added to questions!
		questions[i] = question_list
		return questions

	def get_dialects(self):
		dialects = {}
		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile, dialect='commas')
			dialect_list = [x for x in reader][0][1:]

		for index, x in enumerate(dialect_list):
			dialects[index+1] = x
		return dialects

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

	def get_max_students(self):
		max_students_w_dialect = {}

		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile, dialect='commas')
			# [-1] = Take the last column in the file
			# [1:] = Remove the first element (which in this case is max_students)
			max_student_list = [y for y in reader][-1][1:]

		for d_id, dialect in (self.get_dialects()).iteritems():
			max_students_w_dialect[d_id] = max_student_list[d_id-1]

		return max_students_w_dialect
			
## Run example:
# x = ReadStudentPollCsvFile('studentpoll.csv')
# print x.get_prefixes()		## {1: 'Har med sig', 2: 'Gillar', ....}
# print x.get_questions()		## {1: ['dattamaskin', 'blabla', 'bla'], 2: ['dddd', 'ddd'], ....}
# print x.get_dialects()		## {1: 'Idolbok', 2: 'MacGyver', ....}
# print x.get_points()			## {1: ['dattamaskin', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '', '', '', '1', '', '', '', '', '', '', '2', ''], ....}
# print x.get_max_students()	## {1: '8', 2: '8', ....}