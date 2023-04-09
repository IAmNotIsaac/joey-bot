import tags

from command import CommandInfo, register_command


async def playgame(cmd: CommandInfo):
	pass
    # elif args[0].lower() == "playgame":
    #     if game != None:
    #         message.channel.send("There is currently an active game! Do `endgame` to end it.")

    #     if args[1].lower() == "checkers":
    #         oppoonent = int(args[2][2:-1])
    #         play_game(checkers.CheckersGame(message.channel, message.author.id, oppoonent))

    #     elif args[1].lower() == "dungeon":
    #         team_members = [discord.utils.get(client.get_all_members(), id=int(a[2:-1])) for a in args[2:]]
    #         play_game(dungeon.DungeonGame(message.channel, team_members))

	# def play_game(game_) -> None:
	#     global game
	#     game = game_
register_command(playgame, tags.DEV_TODO)


async def endgame(cmd: CommandInfo):
	pass
    # elif args[0].lower() == "endgame":
    #     game = None
    #     await message.channel.send("Game ended!")
register_command(endgame, tags.DEV_TODO)


async def gamecommand(cmd: CommandInfo):
	pass
    # elif args[0].lower() in ("gc", "gamec", "gamecommand", "game"):
    #     if game != None:
    #         game.__command__(args[1:])
    #     else:
    #         message.channel.send("Currently no active game.")
register_command(gamecommand, tags.DEV_TODO, pseudonyms=["gc", "gamec", "game"])