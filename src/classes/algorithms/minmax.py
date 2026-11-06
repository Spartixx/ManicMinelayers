from classes.manic_mine_layers import ManicMineLayers
from src.classes.algorithms.algorithm import Algorithm


class MinMax(Algorithm):
    def __init__(self, game: ManicMineLayers):
        super().__init__(game)

    def get_move(self, from_position: tuple[int, int]) -> tuple[int, int]:
        pass
