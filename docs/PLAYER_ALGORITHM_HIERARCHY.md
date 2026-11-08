# Technical Documentation - Player and Algorithms 

## Table of contents 
- [1. Human class](#human)
- [2. StupidBot class](#stupidbot)
- [3. Greedy class](#greedy)


### [1.Human class](#human)
#### Overview
The Human class represents a human-controlled player in ManicMinelayers.

It inherits from the Algorithm base class and provides an interface between the game loogic and the graphical user interface (GUI).

Unlike automated algorithms, the Human class does not calculate or evaluate moves? The player selects a cell directly through the game interface.

#### How it works ? 
The class delegates cell selection to the graphical interface. When the player interacts with the game, the GUI handles the selection and returns the chosen cell coordinates.

The selected position is then returned to the calling component.

#### Main methods
- `__init__(game)` : initializes the Human instance and its associated game.
- `get_move(from_position, other_player_position)` : defines the interface for retrieving a move.
- `choose_cell(game_ui)` : delegates cell selection to the GUI and returns the selected coordinates.
- `get_algorithm_type()` : returns AlgorithmType.Human to identify the player type.


### [2. StupidBot class](#stupidbot)
#### Overview
The StupidBot class represents a basic automated player in ManicMinelayers.

It inherits from the Algorithm base class and uses a random selection strategy to choose its moves.

Unlike more advanced algorithms, it does not evaluate possible moves or consider the opponent's position when making a decision.

#### How it works ?
The bot uses Python's random module to randomly select one move from the list of available moves.

The selection is performed using : 

`random.choice(self.game.possible_movs(from_position))`

#### Main methods
- `__init__(game)` : initializes the StupidBot instance and its associated game.
- `get_move(from_position, other_player_position)` : retrieves the available moves and randomly selects one.
- `get_algorithm_type()` : returns AlgorithmType.STUPID_BOT to identify the algorithm.

### [3. Greedy class](#greedy)
#### Overview
The Greedy class represents an algorithm that uses a greedy strategy to select its moves in ManicMinelayers.

It inherits from the Algorithm base class and atttempts to restrict the opponent's mobility by choosing moves that minimize the number of available moves for the opponent. 

Unlike StupidBot, which select randomly, Greedy evaluates each possible move before making a decision.
#### How it works ?
It follows a greedy approach: it selects the move that provides the best immediate result according to a predefined evaluation heuristic.

The goal is to minimize the number of moves available to the opponent after each move.

##### Evaluation Heuristic
The evaluation function measures the opponent's remaining mobility after simulating a candidate move.

The score is defined as : 

Score = number of possible moves available to the opponent after simulated move.

A lower score represents a better move because it leaves the opponent with fewer available options.

#### Main methods 
- `__init__(game)`: initializes the Greedy instance and its associated game.
- `get_algorithm_type()`: returns AlgorithmType.GREEDY to identify the algorithm
- `evaluate_move(from_position, other_player_position, move)` : simulates a candidate move and returns the number of possible moves available to the opponent afterward
- `get_move(from_position, other_player_position)`: evaluates all available moves and returns one of the moves with the lowest score. 
