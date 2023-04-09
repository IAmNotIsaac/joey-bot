## TOOLS ##
# These must be constructed with functions as they are formatted in a specific way.

# A list of hints.
def LIST(hint : str) -> str:
	return "LIST:" + hint

# A union of hints. Acts as implying the type must match one of these hints.
def UNION(*hints : str) -> str:
	return "UNION:" + ":".join(hints)

# Requires an exact string match to parse.
def EXACT(match : str) -> str:
	return "EXACT:" + match

## BUILT-IN TYPES ##
# These values can be cast during the parsing phase.

STR = "STR"	# generic string. internally parses to STR_WORD or STR_FORMATTED
STR_WORD = "STR_WORD"	# a single word, as a string
STR_UNPARSED = "STR_UNPARSED"	# the remainder of the unparsed message, as a string
STR_FORMATTED = "STR_FROMATTED"	# a formatted string (text surrounded with quotes), as a string (obviously)
STR_LIST_UNARGED = "STR_UNARGED"	# the remainder of the message, as a list of strings

NUM = "NUM"	# generic number. interally parses to STR_INT or STR_FLOAT
NUM_INT = "NUM_INT"	# a number with no decimal point
NUM_FLOAT = "NUM_FLOAT"	# a number with a decimal point

## DISCORD SPECIFIC ##
# These values must be cast relevent to context, and after the parsing phase.

USER = "USER"	# a specific user (@)
ROLE = "ROLE"	# a role (@&)
SELECTOR = "SELECTOR"	# "everyone", "here"
USERS = "USERS"	# either LIST:USER, USER, members of ROLE, or those affected by SELECTOR

USER_ID = "USER_ID"	# the id of a specific user
ROLE_ID = "ROLE_ID" # the id of a specific role
# USER_IDS = "USER_IDS" # the ids of specific users

CHANNEL_TEXT = "CHANNEL_TEXT"	# a text channel (#)
CHANNEL_VOICE = "CHANNEL_VOICE"	# a voice channel (#)
CHANNEL_STAGE = "CHANNEL_STAGE"	# a stage channel (#)
CHANNEL_THREAD = "CHANNEL_THREAD"	# a thread (#)
CHANNEL_MESSAGEABLE = "CHANNEL_MESSAGEABLE"	# a dm, text channel, or thread (#)
CHANNEL_VOCAL = "CHANNEL_VOCAL" # a voice or stage channel (#)

CHANNEL_DM_ID = "CHANNEL_DM_ID"	# the id of a dm channel
CHANNEL_TEXT_ID = "CHANNEL_TEXT_ID"	# the id of a text channel
CHANNEL_VOICE_ID = "CHANNEL_VOICE_ID"	# the id of a voice channel
CHANNEL_STAGE_ID = "CHANNEL_STAGE_ID"	# the id of a stage channel
CHANNEL_THREAD_ID = "CHANNEL_THREAD_ID"	# the id of a thread
CHANNEL_MESSAGEABLE_ID = "CHANNEL_MESSAGEABLE_ID"	# the id of a dm, text channel, or thread
CHANNEL_VOCAL_ID = "CHANNEL_VOCAL_ID" # the id of a voice or stage channel


def is_valid(hint: str) -> bool:
	# todo: check for list, union, and exact
	return hint in [
		STR,
		STR_WORD,
		STR_UNPARSED,
		STR_FORMATTED,
		STR_LIST_UNARGED,
		NUM,
		NUM_INT,
		NUM_FLOAT,
		USER,
		ROLE,
		SELECTOR,
		USERS,
		USER_ID,
		ROLE_ID,
		CHANNEL_TEXT,
		CHANNEL_VOICE,
		CHANNEL_STAGE,
		CHANNEL_THREAD,
		CHANNEL_MESSAGEABLE,
		CHANNEL_VOCAL,
		CHANNEL_DM_ID,
		CHANNEL_TEXT_ID,
		CHANNEL_VOICE_ID,
		CHANNEL_STAGE_ID,
		CHANNEL_THREAD_ID,
		CHANNEL_MESSAGEABLE_ID,
		CHANNEL_VOCAL_ID
	]