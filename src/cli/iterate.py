import click

from src.classes.analytics_service import AnalyticsServices


@click.command()
@click.option('--total_games_against_same_player', default=5, type=int)
def iterate(total_games_against_same_player: int = 5):
    AnalyticsServices.iterate_and_write_json(total_games_against_same_player)

if __name__ == "__main__":
    iterate()
