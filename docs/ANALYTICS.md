# Analytics
Analytics can be run by this command:
```
python3 -m src.cli.main --total_games_against_same_player=1
```

This will run game for each possible combination of algorithms, this a ``total_games_against_same_player`` times.
It will generate an analytics file in analytics.json

total_moves of a player for a game_analytics is not implemented yet. Then algorithm hyperparameter should be 
more adjustable.
