from abc import abstractmethod, ABC


class Algorithm(ABC):
    def __init__(self, game):
        self._game = game

    @abstractmethod
    def get_move(self):
        pass

    @property
    def game(self):
        return self._game
