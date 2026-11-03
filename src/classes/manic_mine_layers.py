from typing import Callable

from src.classes.players.player import Player


class ManicMineLayers:
    def __init__(self, player_1: Player, player_2: Player):
        self.player_1 = player_1
        self.player_2 = player_2
        # self.game = ...

    def start(self, display: Callable | None):
        """
        Start the game with the 2 players using a display method or not.
        """
        pass
