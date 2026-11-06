from typing import Literal

from src.schemas.algorithms import AlgorithmType


class AbortionException(Exception):
    pass


class Player:
    def __init__(self, algorithm, number: Literal[1, 2], row: int | None = None):
        self._number: Literal[1, 2] = number
        self._position = [0, 0 if number == 1 else algorithm.game.column_length - 1] if row is None or 0 > row >= algorithm.game.column_length else [row, 0 if number == 1 else algorithm.game.column_length - 1]
        self._algorithm = algorithm

    def play(self, other_player_position: tuple[int, int], game_ui = None) -> tuple[int, int]:
        new_position = self.algorithm.choose_cell(game_ui) if game_ui is not None and self.algorithm.get_algorithm_type() == AlgorithmType.HUMAN else self._algorithm.get_move(self._position, other_player_position)

        if new_position is None:
            raise AbortionException(f"Game is aborted by player {self._number}")

        return new_position

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, new_position: tuple[int, int]):
        self._position = new_position

    @property
    def number(self) -> Literal[1, 2]:
        return self._number

    @property
    def algorithm(self):
        return self._algorithm
