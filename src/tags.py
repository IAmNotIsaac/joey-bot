DEV_TODO = "TODO"	# this command is planned but not yet implemented
DEV_NO_REG = "NO_REG"	# do not register this command
DEV_SECRET = "SECRET"	# dont list this command anywhere

AUTHOR_MASTER = "AUTHOR_MASTER"	# only masters may use
AUTHOR_ADMIN = "AUTHOR_ADMIN"	# only admins may use
AUTHOR_M_OR_A = "AUTHOR_M_OR_A"	# only masters and/or admins may use. equivalent to just specifying both tags

MEDIUM_GUILD = "MEDIUM_GUILD"	# medium must be a server/guild channel
MEDIUM_USER = "MEDIUM_USER"	# medium must be dm/user channel

# ARGS_ALLOW_NONETYPE = "ARGS_ALLOW_NONETYPE:"	# allows an argument to be assigned None if parsing fails


def is_valid(tag: str) -> bool:
	return tag in [
		DEV_TODO,
		DEV_NO_REG,
		DEV_SECRET,
		AUTHOR_MASTER,
		AUTHOR_ADMIN,
		AUTHOR_M_OR_A,
		MEDIUM_GUILD,
		MEDIUM_USER,
		# ARGS_ALLOW_NONE
	]