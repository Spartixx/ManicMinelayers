import math
import random
from typing import Literal

from src.schemas.algorithms import AlgorithmType
from src.schemas.cell_state import CellState
from src.classes.algorithms.algorithm import Algorithm


class MinMax(Algorithm):
    JUMPS = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]
    WIN_SCORE = 10_000

    def __init__(self, game, heuristic: Literal[1, 2] = 2, max_depth: int = 5):
        """
        :param heuristic: Use first or second heuristic method.
        :param max_depth: Max depth to use for MinMax.
        """
        super().__init__(game)
        self.max_depth = max_depth
        self.heuristic = self.heuristic_1 if heuristic == 1 else self.heuristic_2

    def get_move(self, from_position: tuple[int, int], other_player_position: tuple[int, int]) -> tuple[int, int] | None:
        """
        Return the best move found by a MinMax search with alpha and beta pruning.
        """
        my_position = tuple(from_position)
        opponent_position = tuple(other_player_position)
        occupied = self._get_occupied_cells()

        moves = self._available_moves(my_position, occupied)
        if not moves: # There are no moves available anymore.
            return None

        best_moves: list[tuple[int, int]] = []
        best_score = -math.inf
        alpha, beta = -math.inf, math.inf

        for move in moves:
            occupied.add(move) # We are simulating a move so we mark it as occupied
            score = self.mini_max(move, opponent_position, occupied, self.max_depth - 1, alpha, beta, False) # Starting by minimizing as this method already select the best choice. So then, it's the minimizing turn.
            occupied.remove(move) # And unmark it as occupied once we simulated this move using minMax algorithm to calculate the score of this move.

            # Here, we are keeping moves with the best scores which has been already calculated by MinMax.
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

            alpha = best_score

        return random.choice(best_moves) # If 2 moves have the same score, we select it randomly.

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.MINMAX

    def heuristic_1(self, my_position: tuple[int, int], opponent_position: tuple[int, int], occupied: set[tuple[int, int]]) -> float:
        """
        First MinMax heuristic. It calculates the available moves minus opponent available moves.
        """
        my_moves = len(self._available_moves(my_position, occupied))
        opponent_moves = len(self._available_moves(opponent_position, occupied))
        return my_moves - opponent_moves

    def heuristic_2(self, my_position: tuple[int, int], opponent_position: tuple[int, int], occupied: set[tuple[int, int]]) -> float:
        """
        Second MinMax heuristic. It calculates the number of cells each player can reach by chaining jumps, and returns "my" count minus the opponent count. More reachable cells = more future moves before being blocked.
        Mobility is added in case of same cell score for each possible moves.
        """
        my_territory = self._reachable_cells_count(my_position, occupied)
        opponent_territory = self._reachable_cells_count(opponent_position, occupied)
        mobility = len(self._available_moves(my_position, occupied)) - len(self._available_moves(opponent_position, occupied))
        return 100 * (my_territory - opponent_territory) + mobility # The weight of 100 guarantee that the main formula is (my_territory - opponent_territory) and mobility has effect only in case of equality.

    def mini_max(self, my_position: tuple[int, int], opponent_position: tuple[int, int], occupied: set[tuple[int, int]], depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """
        MinMax algorithm using Alpha-beta search. ``maximizing`` is True when maximizing score is needed.
        """
        end_game_score = self._end_game_score(my_position, opponent_position, occupied)

        # This means the game has ended.
        if end_game_score is not None:
            return end_game_score

        # If depth is 0, then, we just use the heuristic without applying algorithm to estimate the best move then ( as it's the depth limit at 0 )
        if depth == 0:
            return self.heuristic(my_position, opponent_position, occupied)

        if maximizing: # Maximizing score turn.
            value = -math.inf
            for move in self._available_moves(my_position, occupied):
                occupied.add(move) # Mark this move as occupied as we are simulating this move.
                value = max(value, self.mini_max(move, opponent_position, occupied, depth - 1, alpha, beta, False)) # Recursively select the max score using MinMax algorithm.
                occupied.remove(move) # And remark it as not occupied as it was just a simulated move.
                if value >= beta: # The minimizing player above already has a branch with a lower score.
                    break
                alpha = max(alpha, value) # Reassign alpha. The value is lower than beta but could be greater than the current alpha value.
            return value

        value = math.inf # Minimizing score turn
        for move in self._available_moves(opponent_position, occupied):
            occupied.add(move) # Mark this move as occupied as we are simulating this move.
            value = min(value, self.mini_max(my_position, move, occupied, depth - 1, alpha, beta, True)) # Recursively select the min score using MinMax algorithm.
            occupied.remove(move) # And remark it as not occupied as it was just a simulated move.
            if value <= alpha: # The maximizing player above already has a branch with a higher score.
                break
            beta = min(beta, value) # Reassign beta if the value get by MinMax is less that the current beta value.

        return value

    def _end_game_score(self, my_position: tuple[int, int], opponent_position: tuple[int, int], occupied: set[tuple[int, int]]) -> float | None:
        """
        Returns the score if the game is over ( a player is blocked ), None if the game is still going on.
        """
        is_min_max_algo_blocked = not self._available_moves(my_position, occupied)
        is_opponent_blocked = not self._available_moves(opponent_position, occupied)

        if is_min_max_algo_blocked and is_opponent_blocked:
            return 0
        if is_opponent_blocked:
            return self.WIN_SCORE
        if is_min_max_algo_blocked:
            return -self.WIN_SCORE
        return None

    def _get_occupied_cells(self) -> set[tuple[int, int]]:
        """
        Returns a set of positions. This set represents the occupied positions of the grid. An occupied position means it's a non empty position and we can't move here.
        """
        return {
            (i, j)
            for i in range(self.game.row_length)
            for j in range(self.game.column_length)
            if self.game.grid[i][j] != CellState.EMPTY
        }

    def _available_moves(self, position: tuple[int, int], occupied: set[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Returns a list of playable moves.
        """
        moves = []
        for jump in self.JUMPS:
            i = position[0] + jump[0]
            j = position[1] + jump[1]
            if 0 <= i < self.game.row_length and 0 <= j < self.game.column_length and (i, j) not in occupied:
                moves.append((i, j))
        return moves

    def _reachable_cells_count(self, position: tuple[int, int], occupied: set[tuple[int, int]]) -> int:
        """
        Count the empty cells reachable from the position with successive knight jumps.
        """
        reachable = set()
        to_visit = [position]
        while to_visit:
            for move in self._available_moves(to_visit.pop(), occupied):
                if move not in reachable:
                    reachable.add(move)
                    to_visit.append(move)
        return len(reachable)
