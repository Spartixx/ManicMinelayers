# MinMax algorithm

## How it works
In the context of ManicMinLayers game and its current implementation, MinMax algorithm plans to find the best move using 
a heuristic to evaluate each cell score.
Then, it finds the best move to play by applying an algorithm working with this heuristic in a specified depth. 

### How the algorithm works
It will simulate two players:
- Max : His job is to maximize his score using a specified heuristic.
- Min : His job is to minimize his score using a specified heuristic. (to simulate the best move of the opponent: 
Best move of opponent = Worst move for the current player)

It will (using recursion) determine the score of a position.
This score is determined by simulate Max and Min play. A negative score for a position means that this position give
advantage to the opponent. By opposition, a positive score means the current player has the advantage, and a higher
score, even more.

### Choices of the heuristics
We chosed 2 heuristics:
- A one counting the max number of play that can be done from a position. A higher one means that using this path, a 
player can survive without being blocked for more turns.
- Another : The difference between available moves if a player moves to this position with the available moves for the
opponent if the player move to this position. So that a higher score means that the current player has more available
moves than the opponent if he plays this move.

The best choice could be determined by iterating games and analyze stats.

## Code explanation
You can find comments on key algorithm code to help you understand how MinMax works. 
