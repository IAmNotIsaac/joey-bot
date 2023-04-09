import tags
import hints

from command import CommandInfo, register_command


async def test(cmd: CommandInfo):
	print("Test command!")
register_command(test)


async def test2(cmd: CommandInfo):
    print("Test command 2!")
register_command(test2)