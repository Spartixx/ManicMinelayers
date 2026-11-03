from abc import abstractmethod, ABC


class Player(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def play(self):
        pass
