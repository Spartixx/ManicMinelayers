from src.schemas.algorithms import AlgorithmType
from src.classes.algorithms.algorithm import Algorithm


class MinMax(Algorithm):
    def __init__(self, game):
        super().__init__(game)

    def get_move(self, from_position: tuple[int, int], other_player_position: tuple[int, int]) -> tuple[int, int]:
        pass

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.MINMAX
