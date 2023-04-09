import time
import tags
import hints

from command import CommandInfo, register_command


async def ilovejoey(cmd: CommandInfo):
    for _ in range(3):
        await cmd.channel.send("i love joey")
register_command(ilovejoey, tags.DEV_SECRET)


async def send_c(cmd: CommandInfo):
    print("send channel")
    await cmd.args["channel"].send(cmd.args["msg"])
register_command(send_c, tags.AUTHOR_MASTER, override_name="send", channel=hints.CHANNEL_TEXT, msg=hints.STR_UNPARSED)


async def send_dm(cmd: CommandInfo):
    print("send dm")
    await cmd.args["user"].send(cmd.args["msg"])
register_command(send_dm, tags.AUTHOR_MASTER, override_name="send", user=hints.USER, msg=hints.STR_UNPARSED)


async def kill(cmd: CommandInfo):
	killer = cmd.author
	victim = cmd.args.victim
	cmd.global_data[victim] = int(time.time())
	if killer == victim:
		await cmd.channel.send("suicide ;(")
	else:
		await cmd.channel.send(f"hey {victim.name}, {killer.name} just killed you lmao")
register_command(kill, tags.MEDIUM_GUILD, victim=hints.USER)


async def score(cmd: CommandInfo):
	pass
    # elif args[0].lower() == "score":
    #     maxn = int(args[1])
    #     target = " ".join(args[2:])
    #     r = random.randrange(0, maxn + 1)

    #     await message.channel.send(f"{target} is a {r} out of {maxn}.")
register_command(score, tags.DEV_TODO)


async def rename(cmd: CommandInfo):
	pass
    # elif args[0].lower() == "rename":
    #     target = ""
    #     idx = len("rename ")

    #     while True:
    #         if message.content[idx] == SEP:
    #             break
    #         else:
    #             target += message.content[idx]

    #         idx += 1

    #         if idx >= len(message.content):
    #             return

    #     new_name = ""
    #     idx += 1

    #     print(target)

    #     while idx < len(message.content):
    #         new_name += message.content[idx]

    #         idx += 1

    #     for member in await guild.fetch_members().flatten():

    #         if member.display_name == target:
    #             await member.edit(nick=new_name)

    #             break
register_command(rename, tags.AUTHOR_MASTER, tags.AUTHOR_MASTER)


async def newchannel(cmd: CommandInfo):
	pass
    # if args[0].lower() == "newchannel":
    #     new_channel_name = args[1] if args[1] else "dumbass-forgot-to-name-me"

    #     await guild.create_text_channel(args[1])
register_command(newchannel, tags.DEV_TODO, tags.AUTHOR_MASTER)


async def purge(cmd: CommandInfo):
	pass
    # elif args[0].lower() == "purge" and message.author.id == 1008492753598038016:
    #     await message.channel.purge(limit=int(args[1]))
register_command(purge, tags.DEV_TODO)


async def delete(cmd: CommandInfo):
	pass
    # elif args[0].lower() == "delete":
    #     async for message in channel.history(limit=200):
    #         if message.id == int(args[1]):
    #             await message.delete()
register_command(delete, tags.DEV_TODO)