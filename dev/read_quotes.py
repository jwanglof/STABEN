class ReadQuotes():
	def __init__(self, filename):
		self.file = open(filename, 'rb').read().splitlines()

	def check_string(self, string):
		check_for = ['staben', 'generalen']
		for x in string.lower().split():
			print [string.lower().find(y) for y in check_for]
				# for y in check_for:
				# 	pos = string.lower().find(y)
				# 	length = len(y)
					# print string[pos:length]
					# print string
		# print string.lower().find([a for a in check_for])

	def get_quotes(self):
		quote_list = []
		# Remove the last period
		for line in self.file:
			if line[-1] is '.':
				line = line[:-1]
			elif line[-2] is '.':
				line = line[:-2]

			# Send string to check_string() instead. FIIIIX!
			quote_list.append(line.replace('"', '').\
				replace('STABEN', '<span class=\'stabenfont\'>STABEN</span>').\
				replace('staben', '<span class=\'stabenfont\'>STABEN</span>').\
				replace('Staben', '<span class=\'stabenfont\'>STABEN</span>').\
				replace('GENERALEN', '<span class=\'stabenfont\'>GENERALEN</span>').\
				replace('generalen', '<span class=\'stabenfont\'>GENERALEN</span>').\
				replace('Generalen', '<span class=\'stabenfont\'>GENERALEN</span>').\
				replace('Nollan', '<span class="nollanfont">Nollan</span>').\
				replace('nollan', '<span class="nollanfont">nollan</span>').\
				replace('Nollans', '<span class="nollanfont">Nollans</span>').\
				replace('nollans', '<span class="nollanfont">nollans</span>').\
				replace('Minus', '<span class="nollanfont">Nollan</span>').\
				replace('minus', '<span class="nollanfont">nollan</span>'))
		return quote_list

## Run example:
# x = ReadQuotes('files/quotes.txt')
# print x.get_quotes()			## ['Fru och barn', 'STABEN kan ro utan vatten', ...]