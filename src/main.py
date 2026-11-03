from typing import Callable

from src.ui.main import display as ui_display


def play_game(display: Callable, player_1, player_2):
    pass # Instantiate a game with player_1 and player_2

if __name__ == '__main__':
    print("It works")
    play_game(ui_display, "human", "stupidbot")
