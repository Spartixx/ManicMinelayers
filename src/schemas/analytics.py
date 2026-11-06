from typing import Literal

from pydantic import BaseModel

from src.schemas.algorithms import AlgorithmType


class PlayerAnalytics(BaseModel):
    win: bool | None
    total_moves: int

class GameAnalytics(BaseModel):
    player_1_analytics: PlayerAnalytics
    player_2_analytics: PlayerAnalytics
    player_winner: Literal[1, 2] | None
    algorithm_winner: AlgorithmType | None
    is_aborted: bool
