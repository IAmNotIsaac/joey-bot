import discord
import globals
import cmd_parser
import tags
import hints
import json

# import games.checkers as checkers
# import games.dungeon as dungeon

from dataclasses import dataclass
from typing import Any, OrderedDict, Union
from command import *

SEP = ","
# CHANNEL_ID = 495479704237637644
# GUILD_ID = 495479704237637642
# VCHANNEL_ID = 495479704237637646

client = discord.Client(intents=discord.Intents.all())


def start():
    print("registering commands...")

    register_command_module("commands.generic")
    register_command_module("commands.voice")
    register_command_module("commands.game")
    register_command_module("commands.dev")
    register_command_module("commands.test")

    print("Commands registered, running client...")
    # print(globals.registered_command_modules)
    # print(globals.user_commands)

    try:
        with open(".secret/key.json", "r") as f:
            key = json.loads(f.read())
            client.run(key)
    except Exception as e:
        print(f"Error running client: {e}")


async def report_error(channel: discord.TextChannel, msg: str) -> None:
    print(msg)
    await channel.send(f"`{msg}`")


@client.event
async def on_ready():
    print("Client is running, have fun!")


@client.event
async def on_message(message):
    text = message.content
    output_errors = False

    if message.author.bot:
        if text[0] == "!" and len(text) > 1:
            text = text[1:]
        else:
            return

    if text[0] == ".":
        if len(text) > 1:
            output_errors = True
            text = text[1:]
        else:
            return

    res = cmd_parser.parse_str_word(text)
    cmd_name = res.value
    text = text[res.end_idx:]
    if cmd_name in globals.user_commands:
        fails = OrderedDict()

        for cmd in globals.user_commands[cmd_name]:
            args = OrderedDict()

            for name, hint in cmd.args.items():
                res = cmd_parser.parse(text, hint)
                if isinstance(res, cmd_parser.ParseFailure):
                    sig = " ".join([cmd_name] + list(cmd.args.values()))
                    msg = f"Failure parsing ({sig}): {res.msg}"
                    fails[sig] = msg
                    continue

                text = text[res.end_idx:]
                value = res.value

                match hint:
                    case hints.USER:
                        value = discord.utils.get(client.get_all_members(), id=value)
                    case hints.ROLE:
                        value = discord.utils.get(await message.guild.fetch_roles(), id=value)
                    case h if h in [hints.CHANNEL_TEXT, hints.CHANNEL_VOICE, hints.CHANNEL_STAGE, hints.CHANNEL_THREAD, hints.CHANNEL_MESSAGEABLE, hints.CHANNEL_VOCAL]:
                        value = discord.utils.get(client.get_all_channels(), id=value)

                args[name] = value

            info = CommandInfo(args, message, message.author, message.guild, message.channel, globals.global_data, cmd)
            res = None
            try:
                res = await cmd.func(info)
            except Exception as e:
                res = CommandFailure(str(e))

            if res == None:
                res = CommandSuccess()

            if isinstance(res, CommandSuccess):
                if res.callback:
                    res.callback(*res.args)

            elif isinstance(res, CommandFailure):
                if output_errors:
                    await report_error(message.channel, res.msg)
                if res.callback:
                    res.callback(*res.args)

            return

        for f in fails.values():
            if output_errors:
                await report_error(message.channel, f)


@client.event
async def on_message_deleted(message):
    print(f"{message.author}: {message.content}")


if __name__ == "__main__":
    start()