from abc import abstractmethod, ABC


class Player(ABC):
    def __init__(self, position: tuple[int, int]):
        self._position = position

    @abstractmethod
    def play(self):
        pass

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, new_position: tuple[int, int]):
        self._position = new_position

