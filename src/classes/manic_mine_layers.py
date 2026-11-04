from typing import Callable

import copy

from src.classes.players.player import Player
from src.enums.cell_state import CellState
from src.enums.game_state import GameState

class ManicMineLayers:
    def __init__(self, player_1: Player, player_2: Player, row_length=5, column_length=10):
        self._player_1 = player_1
        self._player_2 = player_2
        self._row_length = row_length
        self._column_length = column_length
        self._grid = [
            [CellState.EMPTY for _ in range(column_length)]
            for _ in range(row_length)
        ]
        self._current_player = None
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
    def player_1(self):
        return self._player_1
    
    @property
    def player_2(self):
        return self._player_2

    @property
    def current_player(self):
        return self._current_player

    def start(self, display: Callable | None):
        """
        Start the game with the 2 players using a display method or not.
        """
        pass

    def opponent(self, player):
        if player == self.player_1:
            return self._player_2
        return self._player_1
    
    def is_empty(self, i, j):
        """
        Check if square(i, j) is empty or not. Empty means (not busy and not marked)
        """
        if i < 0 or i >= self.m or j < 0 or j >= self.n:
            return False
        if self._grid[i][j] == CellState.EMPTY:
            return True
        return False

    def possible_moves(self, player: Player):
        """
        Save the possible shots for a player by his position and return a list
        """
        jumps = [(-2,-1),(-2,1), (2,-1), (2,1), (-1,-2), (1,-2), (-1,2), (1,2)]
        valid_moves = []
        position = player.position

        for jump in jumps:
            i = position[0] + jump[0]
            j = position[1] + jump[1]
            if self.is_empty(i, j):
                valid_moves.append((i,j))
        return valid_moves

    def play_move(self, player, move):
        """
        PLay the move and mark the old square
        """
        if move not in self.possible_moves(player):
            raise ValueError("Invalid move")

        
        old_position = player.position
        if old_position is not None:
            self._grid[old_position[0]][old_position[1]]= CellState.MARKED

        state = CellState.PLAYER1 if player == self._player_1 else CellState.PLAYER2
        self._grid[move[0]][move[1]] = state
        player.position = move

    def is_blocked(self, player: Player):
        """
        Verify if player can move or not 
        """
        return len(self.possible_moves(player)) == 0

    def game_status(self):
        """
        Check the status of game
        """
        current_blocked = self.is_blocked(self._current_player)
        opponent_blocked = self.is_blocked(self.opponent(self._current_player))

        if current_blocked and opponent_blocked:
            return GameState.DRAW
        elif opponent_blocked and not current_blocked:
            return GameState.CURRENT_WIN
        elif current_blocked and not opponent_blocked:
            return GameState.OPPONENT_WIN
        else:
            return GameState.ONGOING