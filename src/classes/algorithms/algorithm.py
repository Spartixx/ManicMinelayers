from abc import abstractmethod, ABC

class Algorithm(ABC):
    @abstractmethod
    def play(self):
        pass
