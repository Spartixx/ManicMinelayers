from enum import Enum


class AlgorithmType(Enum):
    MCTS = "MCTS"
    MINMAX = "MINMAX"
    HUMAN = "HUMAN"
    GREEDY = "GREEDY"
    STUPID_BOT = "STUPID_BOT"
