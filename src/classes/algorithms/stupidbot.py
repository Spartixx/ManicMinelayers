import random

from src.schemas.algorithms import AlgorithmType
from src.classes.algorithms.algorithm import Algorithm


class StupidBot(Algorithm):
    def __init__(self, game):
        super().__init__(game)

    def get_move(self, from_position: tuple[int, int], other_player_position: tuple[int, int]) -> tuple[int, int]:
        return random.choice(self.game.possible_moves(from_position))

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.STUPID_BOT
