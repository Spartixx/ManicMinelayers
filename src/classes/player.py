from typing import Literal

from src.classes.algorithms.algorithm import Algorithm


class Player:
    def __init__(self, algorithm: Algorithm, number: Literal[1, 2], row: int | None = None):
        self._number: Literal[1, 2] = number
        self._position = [0, 0 if number == 1 else algorithm.game.column_length - 1] if row is None or 0 > row >= algorithm.game.column_length else [row, 0 if number == 1 else algorithm.game.column_length - 1]
        self._algorithm = algorithm

    def play(self):
        self._algorithm.get_move()

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, new_position: tuple[int, int]):
        self._position = new_position

    @property
    def number(self) -> Literal[1, 2]:
        return self._number
