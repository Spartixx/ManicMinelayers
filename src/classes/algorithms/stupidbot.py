import random

from src.classes.manic_mine_layers import ManicMineLayers
from src.classes.algorithms.algorithm import Algorithm


class StupidBot(Algorithm):
    def __init__(self, game: ManicMineLayers):
        super().__init__(game)

    def get_move(self, from_position: tuple[int, int]) -> tuple[int, int]:
        return random.choice(self.game.possible_moves(from_position))
