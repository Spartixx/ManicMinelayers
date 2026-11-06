from abc import abstractmethod, ABC

from src.classes.manic_mine_layers import ManicMineLayers


class Algorithm(ABC):
    def __init__(self, game: ManicMineLayers):
        self._game = game

    @abstractmethod
    def get_move(self, from_position: tuple[int, int]) -> tuple[int, int]:
        pass

    @property
    def game(self) -> ManicMineLayers:
        return self._game
