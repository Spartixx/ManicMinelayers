import click

@click.command()
@click.argument('player_1')
@click.argument('player_2')
def play(player_1: str, player_2: str):
    print(f"Player 1: {player_1}   |   Player 2: {player_2}")
    # TODO
    # - generate a player instance according to each player
    # - Generate a game instance with players
    # - start a game using this game instance ( game.start(display, player_1_instance, player_2_instance) ) -> display come from src/ui/main.py


if __name__ == "__main__":
    play()
