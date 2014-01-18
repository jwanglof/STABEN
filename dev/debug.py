debug_prints = False

## Debug
# 
# @param function Set which function that prints the message
# @param d_print The debug message
# 
# Is used for debug messages and makes it easier to turn it on and off
def debug(function, d_print):
	if debug_prints: print(u'### ' + function + ': ' + d_print)