from pathlib import Path

from src.classes.game_init_service import GameInitService
from src.schemas.algorithms import AlgorithmType
from src.schemas.analytics import GameAnalytics, IterationsAnalytics, GameAnalyticsWithTotalWins, AlgorithmAnalytics


class AnalyticsServices:
    ALGORITHMS = [algorithm_type.value for algorithm_type in AlgorithmType if algorithm_type != AlgorithmType.HUMAN]

    @staticmethod
    def get_games_against_algorithm_for_algorithm(
        for_algorithm_type: AlgorithmType,
        against_algorithm_type: AlgorithmType,
        games_analytics: list[GameAnalytics]
    ) -> list[GameAnalytics]:
        return [game_analytics for game_analytics in games_analytics if game_analytics.player_2_algorithm == AlgorithmType(against_algorithm_type) and game_analytics.player_1_algorithm == AlgorithmType(for_algorithm_type)]

    @staticmethod
    def get_total_game_analytics_against_algorithm_for_algorithm(
        games_analytics: list[GameAnalytics],
        for_algorithm_type: AlgorithmType,
        against_algorithm_type: AlgorithmType
    ) -> GameAnalyticsWithTotalWins:
        filtered_games = [game_analytics for game_analytics in AnalyticsServices.get_games_against_algorithm_for_algorithm(for_algorithm_type, against_algorithm_type, games_analytics)]
        return GameAnalyticsWithTotalWins(
            total_wins=len([1 for game_analytics in filtered_games if game_analytics.player_winner == 1]),
            games=filtered_games
        )

    @staticmethod
    def generate_analytics_from_game_analytics(game_analytics: list[GameAnalytics]) -> IterationsAnalytics:
        def _for(for_algorithm_type: AlgorithmType):
            against = {algorithm_type.lower():AnalyticsServices.get_total_game_analytics_against_algorithm_for_algorithm(game_analytics, for_algorithm_type, algorithm_type) for algorithm_type in AnalyticsServices.ALGORITHMS}
            return AlgorithmAnalytics(total_wins=sum(analytics.total_wins for analytics in against.values()), against=against)

        return IterationsAnalytics(
            mcts=_for(AlgorithmType.MCTS),
            mini_max=_for(AlgorithmType.MINMAX),
            stupid_bot=_for(AlgorithmType.STUPID_BOT),
            greedy=_for(AlgorithmType.GREEDY),
        )

    @staticmethod
    def write_analytics_to_json(iteration_analytics: IterationsAnalytics) -> None:
        with open(Path(__file__).parents[2] / 'analytics.json', 'w') as analytics_file:
            analytics_file.write(iteration_analytics.model_dump_json(indent=2))

    @staticmethod
    def iterate_games(algorithm_1: AlgorithmType, algorithm_2: AlgorithmType, iterations: int = 5) -> list[GameAnalytics]:
        return [GameInitService().init_game(algorithm_1, algorithm_2).start(None, 0) for _ in range(iterations)]

    @staticmethod
    def iterate_all_algorithms_combinations(total_games_against_same_player: int = 5):
        return [game for algorithm_2 in AnalyticsServices.ALGORITHMS for algorithm_1 in AnalyticsServices.ALGORITHMS for game in AnalyticsServices.iterate_games(algorithm_1, algorithm_2, total_games_against_same_player)]

    @staticmethod
    def iterate_and_write_json(total_games_against_same_player: int = 5):
        AnalyticsServices.write_analytics_to_json(
            AnalyticsServices.generate_analytics_from_game_analytics(
                AnalyticsServices.iterate_all_algorithms_combinations(total_games_against_same_player)
            )
        )
