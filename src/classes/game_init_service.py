from src.classes.algorithms.algorithm import Algorithm
from src.classes.algorithms.greedy import Greedy
from src.classes.algorithms.human import Human
from src.classes.algorithms.mcts import MCTS
from src.classes.algorithms.minmax import MinMax
from src.classes.algorithms.stupidbot import StupidBot
from src.classes.manic_mine_layers import ManicMineLayers
from src.classes.player import Player
from src.schemas.algorithms import AlgorithmType


class GameInitService:
    @staticmethod
    def get_algorithm_types(algorithm_1: str, algorithm_2: str) -> tuple[AlgorithmType, AlgorithmType]:
        for algorithm in [algorithm_1, algorithm_2]:
            algorithm_types = [algorithm_type.value for algorithm_type in AlgorithmType]
            if algorithm.upper() not in algorithm_types:
                raise ValueError(f"{algorithm} is not one of {algorithm_types}")

        return [algorithm_1.upper(), algorithm_2.upper()]

    @staticmethod
    def get_algorithm_instance(algorithm_type: AlgorithmType, game: ManicMineLayers) -> Algorithm:
        match (algorithm_type):
            case AlgorithmType.HUMAN.value:
                return Human(game)
            case AlgorithmType.MCTS.value:
                return MCTS(game)
            case AlgorithmType.STUPID_BOT.value:
                return StupidBot(game)
            case AlgorithmType.MINMAX.value:
                return MinMax(game)
            case AlgorithmType.GREEDY.value:
                return Greedy(game)

    def init_game(self, algorithm_1: str, algorithm_2: str) -> ManicMineLayers:
        algorithm_1_type, algorithm_2_type = self.get_algorithm_types(algorithm_1, algorithm_2)
        game = ManicMineLayers()
        game.set_players(
            player_1=Player(algorithm=self.get_algorithm_instance(algorithm_1_type, game), number=1),
            player_2=Player(algorithm=self.get_algorithm_instance(algorithm_2_type, game), number=2),
            current_player=1
        )
        return game
