class CreateGroups():
	def __init__(self):
		top_five = db_commands.admin_get_top_groups_users_only(5)
		dialects = db_commands.get_student_poll_dialects()

	def user_in_group(self, user_id):
		# Check if user_id is in a group
		print top_five
		return

## Run example:
x = CreateGroups()
print x.user_in_group(3)		## {1: 'Har med sig', 2: 'Gillar', ....}