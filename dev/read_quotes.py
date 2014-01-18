import re

## Read quotes
# 
# Reads quotes from a filename
#
# Run example:
# - quotesRead = ReadQuotes('files/quotes.txt')
# - print quotesRead.get_quotes()
#  + ['Fru och barn', 'STABEN kan ro utan vatten', ...]
# - print quotesRead.check_string('STABEN ser allt, Nollan. Generalen har mer skagg!')
#  + '<span class=\'stabenfont\'>STABEN</span> ser allt, <span class=\'nollanfont\'>nollan</span>.  <span class=\'stabenfont\'>GENERALEN</span> har mer skagg!'
#
# @author 	Johan Wänglöf
# @date	2013-08
# @version 	1
class ReadQuotes():
	## The constructor
	# 
	# @param filename Set from which file to read from
	def __init__(self, filename):
		self.file = open(filename, 'rb').read().splitlines()

	## Strip string
	# 
	# @param string Specifies which string to strip the illegal characters from
	# 
	# Strip string from illegal characters
	def strip_string(self, string):
		return string.replace('.', '').replace('"', '')

	## Check string
	# 
	# @param string Specifies which string to check
	#
	# Check a string for special words and replace them with HTML code so they are shown correctly
	def check_string(self, string):
		# Replace with a dict
		# {'staben': '<font staben>'}
		check_for = ['staben', 'generalen', 'nollan', 'minus']

		# Use reg ex instead
		# E.g. periods are removed if it says i.e. '... generalen. Aasd'
		string = string.split()
		for word in string:
			stripped_word = self.strip_string(word).lower()
			if stripped_word in check_for:
				list_index = string.index(word)
				if stripped_word == 'staben':
					string[list_index] = '<span class=\'stabenfont\'>STABEN</span>'
				elif stripped_word == 'generalen':
					string[list_index] = '<span class=\'stabenfont\'>GENERALEN</span>'
				elif stripped_word == 'nollan':
					string[list_index] = '<span class=\'nollanfont\'>nollan</span>'
				elif stripped_word == 'minus':
					string[list_index] = '<span class=\'nollanfont\'>nollan</span>'	
		return ' '.join(string)

	## Get quotes
	# 
	# Get the quotes from the file
	def get_quotes(self):
		quote_list = []

		# Remove the last period
		for line in self.file:
			if line[-1] is '.':
				line = line[:-1]
			elif line[-2] is '.':
				line = line[:-2]

			quote_list.append(self.check_string(line))
		return quote_list