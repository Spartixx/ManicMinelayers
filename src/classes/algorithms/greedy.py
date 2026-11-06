import copy, random

from classes.manic_mine_layers import ManicMineLayers
from src.classes.algorithms.algorithm import Algorithm
from src.classes.player import Player

class Greedy(Algorithm):
    def __init__(self, game: ManicMineLayers, player: Player) -> None:
        super().__init__(game)
        self._player = player 

    @property
    def player(self) -> Player:
        return self._player 
       
    def evaluate_move(self, move: tuple[int, int]) -> int:
        """
        Evaluate the move 
        """
        game = copy.deepcopy(self.game)

        if self.player == self.game.player_1:
            simulated_player = game.player_1
        else:
            simulated_player = game.player_2

        game.play_move(simulated_player, move)
        opponent = game.opponent(simulated_player)
        len_possible_move_opponent = len(game.possible_moves(opponent))
        return len_possible_move_opponent

    def get_move(self) -> tuple[int, int] | None:
        """
        Return the best move 
        """
        moves = self.game.possible_moves(self.player)

        best_moves: list[tuple[int, int]] = []
        best_score = float("inf")

        for move in moves:
            score = self.evaluate_move(move)
            if score < best_score:
                best_score = score
                best_moves.clear()
                best_moves.append(move)
            elif score == best_score:
                best_moves.append(move)
        if not best_moves:
            return None   
        return random.choice(best_moves)
            



        

    
    