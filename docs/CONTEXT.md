# Project Context 

## 1. Project overview 
This project consists of developing a Python implementation of **Manic Minelayers**, a strategy board game created by Frank Truelove in 2000.

The main objective is to implement the game's mechanics and explore different artificial intelligence algorithms (like : **MinMax** and **MCTS**) capable of playing against a human player or other automated players. 

## 2. Game Description 
Manic Minelayers is a two-player strategy game played on a rectangular grid.

Each player controls a pawn of a specific color and takes turns moving across the board. THe movement follows the same rules as a knight in chess. 

### 2.1 Board and Initial Setup 
- By default, the board dimensions are 5 rows and 10 columns 
- The first player initially places their pawn on any empty cell in the first column
- The second player places their pawn on any empty cell in the last column

### 2.2 Movement rules
Players move their pawns according to the knight's movement pattern in chess:
- Two cells horizontally and one cell vertically
- Two cells vertically and one cell horizontally 

A player can only move to an empty cell. Whenever a pawn leaves a cell, that cell becomes permanently occupied by a mark. These marks are shared by both players and cannot be distinguished by color. Marked cells are no longer considered empty and cannot be visited again.

### 2.3 Winning and Draw conditions 
The objective is to block the opponent while preserving at least one available move for yourself.

A player wins their opponent has no legal moves remaining while they can still move.

A draw is also possible when neither player can move.

## 3. Project objectives
The project aims to explore different approaches to artificial intelligence through the implementation and comparison of several player types and decision-making algoritmhs.

The main objectives are: 
- Implement the complete game logic and its rules
- Develop a GUI to display the board and follow the game
- Implement different types of player(huma, stupidbot)
- Explore and compare artificial intelligence algorithms (MinMax, MCTS and Greedy algorithm)
- Evaluate algorithm performance through automated tournaments
- Collect statistics to compare the effectiveness of different stategies

## 4. Graphical User Interface
The project includes a graphical interface developed using **Pygame**
The interface allows to : 
- Visualize the game board and pawn positions
- Follow the progression of the game
- Select and play moves using mouse interaction
- Observe games between different types of players