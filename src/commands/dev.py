import tags
import hints

from command import CommandInfo, register_command


async def hotreloadcommandmodule(cmd: CommandInfo):
	from command import hot_reload_command_modules
	hot_reload_command_modules(cmd.arg("module"))
	await cmd.channel.send(f"Command module '{cmd.arg('module')}' was reloaded.")
register_command(hotreloadcommandmodule, tags.AUTHOR_MASTER, pseudonyms=["hrcm"], module=hints.STR)


async def sourcedump(cmd: CommandInfo):
	pass
register_command(sourcedump)