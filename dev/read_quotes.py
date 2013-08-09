class ReadQuotes():
	def __init__(self, filename):
		self.file = open(filename, 'rb').read().splitlines()

	def get_quotes(self):
		quote_list = []
		for line in self.file:
			if line[-1] is '.':
				line = line[:-1]
			elif line[-2] is '.':
				line = line[:-2]

			quote_list.append(line.replace('"', ''))
		return quote_list

## Run example:
# x = ReadQuotes('files/quotes.txt')
# print x.get_quotes()			## ['Fru och barn', 'STABEN kan ro utan vatten', ...]