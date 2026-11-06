from typing import Callable

import copy

from src.classes.algorithms.algorithm import Algorithm
from src.enums.cell_state import CellState
from src.enums.game_state import GameState

class ManicMineLayers:
    def __init__(
        self,
        algorithm_1: Algorithm,
        algorithm_2: Algorithm,
        algorithm_1_initial_position_y: int = 0,
        algorithm_2_initial_position_y: int = 0,
        row_length=5,
        column_length=10
    ):
        self._algorithm_1 = algorithm_1
        self._algorithm_2 = algorithm_2
        self._current_algorithm = algorithm_1
        self._algorithm_1_position = [algorithm_1_initial_position_y, 1] if 0 <= algorithm_1_initial_position_y < column_length else [0, 0]
        self._algorithm_2_position = [algorithm_2_initial_position_y, 0] if 0 <= algorithm_2_initial_position_y < column_length else [0, 1]

        self._row_length = row_length
        self._column_length = column_length
        self._grid = [
            [CellState.EMPTY for _ in range(column_length)]
            for _ in range(row_length)
        ]

        self._grid[self._algorithm_1_position[0]][self._algorithm_1_position[1]] = CellState.PLAYER1
        self._grid[self._algorithm_2_position[0]][self._algorithm_2_position[1]] = CellState.PLAYER2

    @property
    def row_length(self):
        return self._row_length

    @property
    def column_length(self):
        return self._column_length

    @property
    def grid(self):
        return copy.deepcopy(self._grid)

    @property
    def algorithm_1(self):
        return self._algorithm_1
    
    @property
    def algorithm_2(self):
        return self._algorithm_2

    @property
    def current_algorithm(self):
        return self._current_algorithm

    def start(self, display: Callable | None):
        """
        Start the game with the 2 algorithms using a display method or not.
        """
        pass

    def opponent(self, algorithm):
        if algorithm == self.algorithm_1:
            return self._algorithm_2
        return self._algorithm_1
    
    def is_empty(self, i, j):
        """
        Check if square(i, j) is empty or not. Empty means (not busy and not marked)
        """
        if i < 0 or i >= self.row_length or j < 0 or j >= self.column_length:
            return False
        if self._grid[i][j] == CellState.EMPTY:
            return True
        return False

    def possible_moves(self, algorithm: Algorithm) -> tuple[int, int]:
        """
        Save the possible shots for a algorithm by his position and return a list
        """
        jumps = [(-2,-1),(-2,1), (2,-1), (2,1), (-1,-2), (1,-2), (-1,2), (1,2)]
        valid_moves = []
        position = self._algorithm_1_position if self._current_algorithm == self._algorithm_1 else self._algorithm_2_position

        for jump in jumps:
            i = position[0] + jump[0]
            j = position[1] + jump[1]
            if self.is_empty(i, j):
                valid_moves.append((i,j))

        return valid_moves

    def play_move(self, algorithm: Algorithm, move: tuple[int, int]) -> None:
        """
        Play the move and mark the old square
        """
        if move not in self.possible_moves(algorithm):
            raise ValueError("Invalid move")
        
        old_position = self._algorithm_1_position if self._current_algorithm == self._algorithm_1 else self._algorithm_2_position
        self._grid[old_position[0]][old_position[1]]= CellState.MARKED

        state = CellState.PLAYER1 if algorithm == self._algorithm_1 else CellState.PLAYER2
        self._grid[move[0]][move[1]] = state
        algorithm.position = move

    def is_blocked(self, algorithm: Algorithm) -> bool:
        """
        Verify if algorithm can move or not 
        """
        return len(self.possible_moves(algorithm)) == 0

    def game_status(self) -> GameState:
        """
        Check the status of game
        """
        current_blocked = self.is_blocked(self._current_algorithm)
        opponent_blocked = self.is_blocked(self.opponent(self._current_algorithm))

        if current_blocked and opponent_blocked:
            return GameState.DRAW
        elif opponent_blocked and not current_blocked:
            return GameState.CURRENT_WIN
        elif current_blocked and not opponent_blocked:
            return GameState.OPPONENT_WIN
        else:
            return GameState.ONGOING