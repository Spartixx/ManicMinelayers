from src.classes.players.player import Player


class Human(Player):
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)

    def play(self):
        pass
