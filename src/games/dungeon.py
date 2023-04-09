import asyncio
import nest_asyncio

from game import GameInterface
from discord import File
from PIL import Image

nest_asyncio.apply()


class GameState:
	pass


class DungeonGame(GameInterface):
	def __init__(self, channel, members) -> None:
		self.channel = channel
		self.members = members
		print(members)