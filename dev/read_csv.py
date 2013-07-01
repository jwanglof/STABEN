import csv

###
# Need to add the questions to a list
# since dict's aren't ordered
###
class ReadStudentPollCsvFile():
	prefixes = {}
	questions = {}

	def __init__(self, filename):
		self.filename = filename

	# Check so that row doesn't contain any 'illegal' characters
	def check(self, row):
		if row[:1] == ',' or row == 'SUmma' or row == '':
			return False
		else:
			return True

	def get_prefixes(self):
		i = 1
		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if self.check(row[0]) and row[0][:1].isupper():
					self.prefixes[i] = row[0]
					i += 1
		return self.prefixes

	def get_questions(self):
		i = 0
		o = 0
		tmp_list = []

		with open(self.filename, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if self.check(row[0]) and row[0][:1].isupper():
					if i > 0:
						self.questions[i] = tmp_list
						tmp_list = []
					i += 1

				if self.check(row[0]) and row[0][:1].islower():
					tmp_list.append(row[0])

		# Need this so the last list is added to self.questions!
		self.questions[i] = tmp_list
		return self.questions

## Run example:
# x = ReadStudentPollCsvFile('studentpoll.csv')
# print x.get_prefixes()
# print x.get_questions()
#
## Will return:
## 1: ['dattamaskin', 'blabla', 'bla'], 2: ['dddd', 'ddd'] etc