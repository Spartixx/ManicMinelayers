# ManicMinelayers

Make AI playing ManicMinelayers with each others !

## Available players

- stupidbot ( play with random choices )
- human ( You play )
- minmax
- MCTS
- greedy

## Technical documentation 

- [Project Context](docs/CONTEXT.md)
- [Project Structure](docs/STRUCTURE.md)
- [Interpretations of statistics](docs/ANALYTICS.md)
- [Main class](docs/MAIN_CLASS.md)
- [Player and Algorithm hierarchy](docs/PLAYER_ALGORITHM_HIERARCHY.md)
- [MinMax ](docs/MINMAX.md)
- [MCTS](docs/MCTS.md)

## Usage

### Requirements
This python project requires you to install some packages:

#### First, create a virtual environment 
```shell
python3 -m venv .venv
```

#### Then, enter in this virtual environment
Mac / Linux
```shell
source .venv/bin/activate
```

Windows
```shell
.venv/Scripts/activate
```

#### Install required packages
```shell
pip install -r requirements.txt
```

---

### Play against an AI
```shell
python3 -m src.cli.play human stupid_bot
```

### Make 2 AI play with each others and look at the game
```shell
python3 -m src.cli.play minmax stupid_bot
```

- use ``--ai_speed=<a_float>`` to adjust AI play speed in the game.
- use ``--show_ui`` to display or not the ui if 2 players with AI algorithms are playing. By default, if 2 players with 
AI algorithms are playing, UI will not be displayed.

#### Example
```shell
python3 -m src.cli.play minmax stupid_bot --show_ui --ai_speed=0.2
```

---

## Contributors
- Nicolas Macrez
- El Asad Ben Nordine Hamissi Youssouf
- Cédric Richard Bintcha Piame
