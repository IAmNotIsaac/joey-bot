# keeps track of all registered modules to ensure a module is never registered
# twice, and as well allows for hot reloading.
registered_command_modules = {}

# all user commands.
user_commands = {}

# global data. this data is saved (todo). this data is for commands.
global_data = {}

# the settings of the bot. this data is saved (todo).
configuration = {
	"masters_of_mischief": [328665978466729985]
}