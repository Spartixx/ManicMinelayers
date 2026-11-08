from time import sleep
from typing import Literal

import copy

from src.classes.player import AbortionException
from src.schemas.algorithms import AlgorithmType
from src.schemas.analytics import GameAnalytics, PlayerAnalytics
from src.classes.player import Player
from src.schemas.cell_state import CellState
from src.schemas.game_state import GameState


class ManicMineLayers:
    def __init__(self, row_length=5, column_length=10):
        self._row_length = row_length
        self._column_length = column_length
        self._grid = [
            [CellState.EMPTY for _ in range(column_length)]
            for _ in range(row_length)
        ]
        self._grid[0][0] = CellState.MARKED
        self._player_1 = None
        self._player_2 = None
        self._current_player: Player | None = None
        self._game_state: GameState = GameState.ONGOING

    def set_players(self, player_1: Player, player_2: Player, current_player: Literal["1", "2"]):
        self._player_1 = player_1
        self._player_2 = player_2
        self._current_player = self._player_1 if current_player == 1 else self._player_2
        self._grid[self._player_1.position[0]][self._player_1.position[1]] = CellState.PLAYER1
        self._grid[self._player_2.position[0]][self._player_2.position[1]] = CellState.PLAYER2

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
    def player_1(self) -> Player | None:
        return self._player_1
    
    @property
    def player_2(self) -> Player | None:
        return self._player_2

    @property
    def current_player(self) -> Player | None:
        return self._current_player

    def _check_player_are_set(self):
        if self._current_player is None:
            raise Exception("Players are not set.")

    def _get_aborted_game_analytics(self) -> GameAnalytics:
        return GameAnalytics(
            player_1_analytics=PlayerAnalytics(
                total_moves=1,
                win=False if self._current_player == self.player_1 else True,
            ),
            player_2_analytics=PlayerAnalytics(
                total_moves=1,
                win=True if self._current_player == self.player_1 else False,
            ),
            is_aborted=True,
            player_winner=self.opponent(self._current_player).number,
            algorithm_winner=self.opponent(self._current_player).algorithm.get_algorithm_type(),
        )

    def _get_game_winner(self) -> Player | None:
        last_player = self.opponent(self._current_player)
        if self._game_state == GameState.CURRENT_WIN:
            return last_player
        if self._game_state == GameState.OPPONENT_WIN:
            return self._current_player
        return None

    def _get_game_analytics(self) -> GameAnalytics:
        winner = self._get_game_winner()
        return GameAnalytics(
            player_1_analytics=PlayerAnalytics(
                total_moves=1,
                win=None if winner is None else winner == self._player_1,
            ),
            player_2_analytics=PlayerAnalytics(
                total_moves=1,
                win=None if winner is None else winner == self._player_2,
            ),
            is_aborted=False,
            player_winner=None if winner is None else winner.number,
            algorithm_winner=None if winner is None else winner.algorithm.get_algorithm_type(),
        )

    def start(self, game_ui = None, ai_speed: float = 2) -> GameAnalytics:
        """
        Start the game with the 2 players using a display method or not.

        :param game_ui: If the UI should be shown even if 2 players with AI algorithms are playing with each others ( useful to follow the game ). If you are iterating games to get analytics, you should set this Param to an instance of ``GameView``. Please note that UI is always displayed if one of the 2 players is a human even if this param is set to False.
        :param ai_speed: Speed of the AI. It represents the time that should be elapsed before a player with an AI algorithm play ( not including algorithm elapsed time to choose next move ). It can be useful to follow a game played by 2 players with AI algorithms. Otherwise, the game would be too fast to be followed.
        """
        self._check_player_are_set()

        while self._game_state == GameState.ONGOING and self._current_player is not None:
            if game_ui:
                game_ui.display()

            try:
                if self._current_player.algorithm.get_algorithm_type() == AlgorithmType.HUMAN:
                    def _play_human():
                        try:
                            self.play_move(self._current_player, self._current_player.play(self.opponent(self._current_player).position, game_ui))
                        except ValueError:
                            _play_human()
                    _play_human()
                else:
                    sleep(ai_speed)
                    self.play_move(self._current_player, self._current_player.play(self.opponent(self._current_player).position))
            except AbortionException:
                return self._get_aborted_game_analytics()

            self.set_game_state()
            self._current_player = self.opponent(self.current_player)

        return self._get_game_analytics()

    def opponent(self, player) -> Player:
        self._check_player_are_set()

        if player == self.player_1:
            return self._player_2
        return self._player_1
    
    def is_empty(self, i, j):
        """
        Check if square(i, j) is empty or not. Empty means (not busy and not marked)
        """
        if i < 0 or i >= self.row_length or j < 0 or j >= self.column_length:
            return False
        if self._grid[i][j] == CellState.EMPTY:
            return True
        return False

    def possible_moves(self, position: tuple[int, int]) -> tuple[int, int]:
        """
        Save the possible shots for a player by his position and return a list
        """
        jumps = [(-2,-1),(-2,1), (2,-1), (2,1), (-1,-2), (1,-2), (-1,2), (1,2)]
        valid_moves = []

        for jump in jumps:
            i = position[0] + jump[0]
            j = position[1] + jump[1]
            if self.is_empty(i, j):
                valid_moves.append((i,j))

        return valid_moves

    def get_player_from_position(self, position: tuple[int, int]) -> Player | None:
        if self.player_2.position == position:
            return self._player_2
        if self.player_1.position == position:
            return self._player_1
        return None

    def play_move(self, player: Player, move: tuple[int, int]) -> None:
        """
        Play the move and mark the old square
        """
        if move not in self.possible_moves(player.position):
            raise ValueError("Invalid move")
        
        old_position = player.position
        if old_position is not None:
            self._grid[old_position[0]][old_position[1]]= CellState.MARKED

        state = CellState.PLAYER1 if player == self._player_1 else CellState.PLAYER2
        self._grid[move[0]][move[1]] = state
        player.position = move

    def is_blocked(self, player: Player) -> bool:
        """
        Verify if player can move or not 
        """
        return len(self.possible_moves(player.position)) == 0

    def set_game_state(self) -> None:
        """
        Set the status of the game by checking at player available moves.
        """
        current_blocked = self.is_blocked(self._current_player)
        opponent_blocked = self.is_blocked(self.opponent(self._current_player))

        if current_blocked and opponent_blocked:
            self._game_state = GameState.DRAW
        elif opponent_blocked and not current_blocked:
            self._game_state = GameState.CURRENT_WIN
        elif current_blocked and not opponent_blocked:
            self._game_state = GameState.OPPONENT_WIN
        else:
            self._game_state = GameState.ONGOING
