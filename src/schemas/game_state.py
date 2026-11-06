from enum import Enum

class GameState(Enum):
    ONGOING = "Continue"
    CURRENT_WIN = "Joueur courant a gagné"
    OPPONENT_WIN = "Adversaire a gagné"
    DRAW = "Match nul"
    