import globals
import inspect
import importlib
import discord

from dataclasses import dataclass, field
from typing import Any, Callable, OrderedDict, Union
from types import NoneType


@dataclass
class CommandSuccess:
    callback: Callable = None
    args: list[Any] = field(default_factory=list)


@dataclass
class CommandFailure:
    msg: str
    callback: Callable = None
    args: list[Any] = field(default_factory=list)


CommandResult = Union[CommandSuccess, CommandFailure]
CommandReturn = Union[CommandSuccess, CommandFailure, NoneType]


@dataclass
class Command:
    func: Callable
    names: set[str]
    help: str
    args: OrderedDict[str, Any]
    tags: list[str]
    module_name: str


@dataclass
class CommandInfo:
    args: OrderedDict[str, Any]
    message: discord.Message
    author: Union[discord.User, discord.Member]
    guild: discord.Guild
    channel: discord.TextChannel
    # vchannel: discord.VoiceChannel
    global_data: dict
    command: Command

    def arg(self, name: str) -> Any:
        try:
            return self.args[name]
        except:
            return None


def register_command(func, *tags, override_name="", pseudonyms=[], help="Undocumentated", **args) -> None:
    module_name = inspect.getouterframes(inspect.currentframe())[1].frame.f_globals['__name__']

    if override_name:
        func.__name__ = override_name

    name = func.__name__
    cmd = Command(func, set([name] + pseudonyms), help, args, tags, module_name)

    if name not in globals.user_commands:
        globals.user_commands[name] = []

    # add command to list (ensure only one instance)
    if cmd not in globals.user_commands[name]:
        globals.user_commands[name].append(cmd)
    for p in pseudonyms:
        if p not in globals.user_commands:
            globals.user_commands[p] = []

        if cmd not in globals.user_commands[p]:
            globals.user_commands[p].append(cmd)

    print(f"\t- Registered command '{name}'.")


def register_command_module(name: str) -> None:
    if name in globals.registered_command_modules:
        print(f"Module '{name}' was previously registered. Consider hot-reloading instead. Ignoring request.")
        return

    print(f"Registering command module '{name}'...")

    module = importlib.import_module(name)
    globals.registered_command_modules[name] = module

    print(f"Command module '{name}' registered.")


def hot_reload_command_modules(name: str):
    if name not in globals.registered_command_modules:
        print(f"Module {name} must first be registered before it can be hot-reloaded. Ignoring request.")
        return

    print(f"Beginning hot-reload of command module '{name}'...")
    print(f"Removing command module '{name}' commands...")

    # remove commands from command module
    for cmd_name, cmds in globals.user_commands.items():
        for cmd in cmds:
            if cmd.module_name == name:
                print(f"\t- Removing command '{cmd_name}' from index.")
                globals.user_commands[cmd_name].remove(cmd)

    print(f"Command module '{name}' commands removed.")
    print(f"Cleaning up empty commands...")

    # clean up empty commands
    for cmd_name in list(globals.user_commands.keys()):
        if cmd_name in globals.user_commands and len(globals.user_commands[cmd_name]) == 0:
            print(f"\t- Cleaning empty command '{cmd_name}'")
            del globals.user_commands[cmd_name]

    print(f"Empty commands cleaned.")
    print(f"Registering command module '{name}' commands...")

    module = globals.registered_command_modules[name]
    globals.registered_command_modules[name] = importlib.reload(module)

    print(f"Command module commands '{name}' registered.")
    print(f"Hot-reload of command module '{name}' finished.")