from abc import abstractmethod, ABC

from src.schemas.algorithms import AlgorithmType


class Algorithm(ABC):
    def __init__(self, game):
        self._game = game

    @abstractmethod
    def get_move(self, from_position: tuple[int, int]) -> tuple[int, int] | None:
        """
        get next algorithm move according to a specified "from_position". If results is None, it means the game is aborted.
        """
        pass

    @abstractmethod
    def get_algorithm_type(self) -> AlgorithmType:
        """
        get algorithm type
        """
        pass

    @property
    def game(self):
        return self._game
