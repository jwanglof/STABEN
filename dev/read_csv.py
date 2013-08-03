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
		if row[:1] == ',' or row == 'SUmma' or row == '':
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
		i = 0
		o = 0
		tmp_list = []
		questions = {}

		# Change staben to <span class='stabenfont'>STABEN</span>
		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if self.check(row[0]) and row[0][:1].isupper():
					if i > 0:
						questions[i] = tmp_list
						tmp_list = []
					i += 1

				if self.check(row[0]) and row[0][:1].islower():
					tmp_list.append(row[0])

		# Need this so the last list is added to questions!
		questions[i] = tmp_list
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


## Run example:
# x = ReadStudentPollCsvFile('studentpoll.csv')
# print x.get_prefixes()	## {1: 'Har med sig', 2: 'Gillar', ....}
# print x.get_questions()	## {1: ['dattamaskin', 'blabla', 'bla'], 2: ['dddd', 'ddd'], ....}
# print x.get_dialects()	## {1: 'Idolbok', 2: 'MacGyver', ....}
# print x.get_points()		## {1: ['dattamaskin', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '', '', '', '1', '', '', '', '', '', '', '2', ''], ....}