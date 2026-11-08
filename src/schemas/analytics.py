from typing import Literal

from pydantic import BaseModel

from src.schemas.algorithms import AlgorithmType


class PlayerAnalytics(BaseModel):
    win: bool | None
    total_moves: int # Not implemented yet.

class GameAnalytics(BaseModel):
    player_1_algorithm: AlgorithmType
    player_2_algorithm: AlgorithmType
    player_1_analytics: PlayerAnalytics
    player_2_analytics: PlayerAnalytics
    player_winner: Literal[1, 2] | None
    algorithm_winner: AlgorithmType | None
    is_aborted: bool

class GameAnalyticsWithTotalWins(BaseModel):
    total_wins: int
    games: list[GameAnalytics]

class AlgorithmAnalytics(BaseModel):
    total_wins: int
    against: dict[str, GameAnalyticsWithTotalWins]

class IterationsAnalytics(BaseModel):
    mcts: AlgorithmAnalytics
    mini_max: AlgorithmAnalytics
    stupid_bot: AlgorithmAnalytics
    greedy: AlgorithmAnalytics
