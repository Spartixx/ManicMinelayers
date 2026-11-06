from src.schemas.algorithms import AlgorithmType
from src.classes.algorithms.algorithm import Algorithm


class Human(Algorithm):
    def __init__(self, game):
        super().__init__(game)

    def get_move(self, from_position: tuple[int, int]) -> tuple[int, int] | None:
        pass

    def choose_cell(self, game_ui) -> tuple[int, int] | None:
        return game_ui.choose_cell()

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.HUMAN
