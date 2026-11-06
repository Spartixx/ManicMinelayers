import copy, random

from src.schemas.algorithms import AlgorithmType
from src.classes.algorithms.algorithm import Algorithm

class Greedy(Algorithm):
    def __init__(self, game) -> None:
        super().__init__(game)

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.GREEDY

    def evaluate_move(self, from_position: tuple[int, int], other_player_position: tuple[int, int], move: tuple[int, int]) -> int:
        """
        Evaluate the move
        """
        game = copy.deepcopy(self.game)

        game.play_move(game.get_player_from_position(from_position), move)
        len_possible_move_opponent = len(game.possible_moves(other_player_position))
        return len_possible_move_opponent

    def get_move(self, from_position: tuple[int, int], other_player_position: tuple[int, int]) -> tuple[int, int] | None:
        """
        Return the best move 
        """
        moves = self.game.possible_moves(from_position)

        best_moves: list[tuple[int, int]] = []
        best_score = float("inf")

        for move in moves:
            score = self.evaluate_move(from_position, other_player_position, move)
            if score < best_score:
                best_score = score
                best_moves.clear()
                best_moves.append(move)
            elif score == best_score:
                best_moves.append(move)
        if not best_moves:
            return None   
        return random.choice(best_moves)
