import asyncio
import nest_asyncio

from discord import File
from PIL import Image
from game import GameInterface

nest_asyncio.apply()


class Tile:
	NULL = -1
	EMPTY = 0
	PLAYER1 = 1
	PLAYER2 = 2
	PLAYER1K = 3
	PLAYER2K = 4

	def __init__(self, pos) -> None:
		self.state = Tile.EMPTY
		self.pos = pos

		self.assume_default()


	def assume_default(self) -> None:
		self.state = Tile.EMPTY

		if (self.pos[0] % 2 + self.pos[1] % 2) % 2 == 0:
			if self.pos[1] < 3:
				self.state = Tile.PLAYER2

			if self.pos[1] >= 5:
				self.state = Tile.PLAYER1


	def is_empty(self) -> bool:
		return self.state == Tile.EMPTY


	def is_player1(self) -> bool:
		return self.state in (Tile.PLAYER1, Tile.PLAYER1K)


	def is_player2(self) -> bool:
		return self.state in (Tile.PLAYER2, Tile.PLAYER2K)


	def is_king(self) -> bool:
		return self.state in (Tile.PLAYER1K, Tile.PLAYER2K)


	def __str__(self) -> str:
		return {
			Tile.EMPTY: ".",
			Tile.PLAYER1: "X",
			Tile.PLAYER2: "O"
		}[self.state]


class GameState:
	def __init__(self, player1, player2) -> None:
		self.player1 = player1
		self.player2 = player2
		self.turn = player1
		self.tiles = [[Tile((x, y)) for y in range(8)] for x in range(8)]
		self.error = ""


	# Returns whether or not the move is valid and consequently, carried out
	def move(self, pos1, pos2) -> bool:
		self.error = ""
		t1 = self.get_tile(pos1)
		t2 = self.get_tile(pos2)
		pdir = self.get_player_direction()
		passed = False
		ext_break = False

		if self.player_owns(self.turn, t1) and t2.state == Tile.EMPTY:
			dirs = [pdir]
			if t1.is_king():
				dirs.append(-pdir)

			for i in dirs:
				if ext_break:
					break

				left = (pos1[0] - 1, pos1[1] + i)
				right = (pos1[0] + 1, pos1[1] + i)

				sleft = (pos1[0] - 2, pos1[1] + i * 2)
				sright = (pos1[0] + 2, pos1[1] + i * 2)

				if pos2 in [left, right]:
					new_state = t1.state

					if (t1.is_player1() and pos2[1] == 0) or (t1.is_player2() and pos2[1] == 7):
						new_state = self.get_player_tile_king_state()

					self.set_tile_state(pos1, Tile.EMPTY)
					self.set_tile_state(pos2, new_state)
					passed = True

				else:
					valid = False
					for d in [(sleft, left), (sright, right)]:
						if pos2 == d[0]:
							if self.enemy_owns(self.turn, self.get_tile(d[1])):
								new_state = t1.state

								if (t1.is_player1() and pos2[1] == 0) or (t1.is_player2() and pos2[1] == 7):
									new_state = self.get_player_tile_king_state()

								self.set_tile_state(pos1, Tile.EMPTY)
								self.set_tile_state(pos2, new_state)
								self.set_tile_state(d[1], Tile.EMPTY)
								passed = False
								valid = True
								ext_break = True
								self.error = ""

								break

							else:
								self.error = "Cannot skip to tile, enemy not in-between."

					if not valid:
						self.error = ""
						# self.error = "Cannot move to here. Must be diagonally adjacent, or a skip."

		else:
			self.error = "Cannot move piece that is not your own."

		if passed:
			self.turn = self.get_next_turn(self.turn)


	def get_tile(self, pos) -> Tile:
		return self.tiles[pos[0]][pos[1]]


	def set_tile_state(self, pos, state) -> Tile:
		self.tiles[pos[0]][pos[1]].state = state


	def player_owns(self, player, tile) -> bool:
		return (
			(player == self.player1 and tile.is_player1()) or
			(player == self.player2 and tile.is_player2())
		)


	def enemy_owns(self, player, tile) -> bool:
		return (
			(player == self.player1 and tile.is_player2()) or
			(player == self.player2 and tile.is_player1())
		)


	def get_player_direction(self) -> int:
		return {
			self.player1: -1,
			self.player2: 1
		}[self.turn]


	def get_player_tile_state(self) -> int:
		return {
			self.player1: Tile.PLAYER1,
			self.player2: Tile.PLAYER2
		}[self.turn]


	def get_player_tile_king_state(self) -> int:
		return {
			self.player1: Tile.PLAYER1K,
			self.player2: Tile.PLAYER2K
		}[self.turn]


	def get_next_turn(self, player) -> int:
		return {
			self.player1: self.player2,
			self.player2: self.player1
		}[player]


	def get_winner(self) -> int:
		p1_count = 0
		p2_count = 0

		for l in self.tiles:
			for t in l:
				if t.is_player1():
					p1_count += 1
				elif t.is_player2():
					p2_count += 1

		if p1_count == 0:
			return self.player2
		elif p2_count == 0:
			return self.player1

		return 0


class CheckersGame(GameInterface):
	def __init__(self, channel, player1, player2) -> None:
		self.channel = channel
		self.gamestate = GameState(player1, player2)
		# self.gamestate.set_tile_state((2, 4), Tile.PLAYER2)
		# self.gamestate.set_tile_state((5, 1), Tile.PLAYER1)
		asyncio.run(self.update_board())


	def __command__(self, args) -> None:
		if self.gamestate.get_winner() != 0:
			self.channel.send("Game is over! Do `endgame`, please.")

		if args[0] == "move".lower():
			start = None
			end = None
			try:
				start = CheckersGame.convert_to_pos(args[1])
				try:
					end = CheckersGame.convert_to_pos(args[2])
				except:
					self.gamestate.error = f"Cannot convert 2nd argument to tile position. ({args[2]})"
			except:
				self.gamestate.error = f"Cannot convert 1st argument to tile position. ({args[1]})"

			if start and end:
				self.gamestate.move(start, end)

			asyncio.run(self.update_board())


		elif args[0] == "pass".lower():
			self.gamestate.turn = self.gamestate.get_next_turn(self.gamestate.turn)
			asyncio.run(self.update_board())


		elif args[0] == "show".lower():
			asyncio.run(self.update_board())


	def convert_to_pos(pos):
		row = {
			"a": 0, "b": 1, "c": 2, "d" : 3, "e": 4, "f": 5, "g": 6, "h": 7
		}[pos[0].lower()]
		column = int(pos[1]) - 1
		return (row, column)


	async def update_board(self) -> None:
		res = f"Error! `{self.gamestate.error}`\n" if self.gamestate.error != "" else ""
		res += f"<@{self.gamestate.turn}>'s turn:\n"
		# res += "```\n"
		# res += "  A B C D E F G H"
		# for i in range(8):
		# 	res += f"\n{i + 1}"
		# 	for x in range(8):
		# 		res += f" {self.gamestate.get_tile((x, i))}"
		# res += "\n```"

		board = "checkerboard"

		winner = self.gamestate.get_winner()
		if winner != 0:
			res = f"<@{self.gamestate.get_next_turn(self.gamestate.turn)}> is the winner!"
			board = "checkerboardgameover"

		with Image.open(f"assets/{board}.png") as im:
			p1 = Image.open("assets/black_piece.png")
			p2 = Image.open("assets/red_piece.png")
			p3 = Image.open("assets/black_king_piece.png")
			p4 = Image.open("assets/red_king_piece.png")

			for l in self.gamestate.tiles:
				for t in l:
					ppos = (t.pos[0] * 32 + 32, t.pos[1] * 32 + 32)
					piece = None

					if t.is_player1():
						piece = p1
						if t.is_king():
							piece = p3
					elif t.is_player2():
						piece = p2
						if t.is_king():
							piece = p4

					if piece:
						im.paste(piece, (ppos[0], ppos[1], ppos[0] + 32, ppos[1] + 32), piece)

			im = im.resize((im.width * 2, im.height * 2), Image.Resampling.NEAREST)
			im.save("assets/_checkersgamestate.png")

		await self.channel.send(res, file=File("assets/_checkersgamestate.png"))
