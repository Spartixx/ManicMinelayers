# Structure of the ManicMinelayers project

This document presents the organization of the Python project
**ManicMinelayers**, describing the role of the main files and
files.

``` bash
ManicMinelayers/
├── docs/ # contains all techinal documentation files
├── src/
│   ├── classes/
│   │   ├── algorithms/
│   │   │   ├── __init__.py
│   │   │   ├── algorithm.py # contains the base class common to algorithms.
│   │   │   ├── greedy.py # contains greedy algorithm
│   │   │   ├── human.py # contains human class
│   │   │   ├── mcts.py # contains MCTS(Monte Carlo Tree Search) algorithm
│   │   │   ├── minmax.py # contains minmax algorithm
│   │   │   └── stupidbot.py # contains stupidbot class
│   │   ├── __init__.py
│   │   ├── manic_mine_layers.py # contains manicminelayers class
│   │   ├── player.py # contains player class
│   │   └── vertex.py # 
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── algorithms.py # define all algorithm type
│   │   ├── analytics.py
│   │   ├── cell_state.py # define different state of cell
│   │   └── game_state.py # define different state of a game 
│   └── ui/
│       ├── __init__.py
│       └── game_view.py # manage the GUI
├── .gitignore # tells Git which files and folders to ignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── Makefile 
├── README.dev.md
├── README.md
└── requirements.txt # list of dependencies 
```

