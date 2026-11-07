import copy
import math
import random

from src.classes.algorithms.algorithm import Algorithm
from src.classes.vertex import Vertex
from src.schemas.algorithms import AlgorithmType
from src.schemas.game_state import GameState


class MCTS(Algorithm):
    def __init__(self, game, iterations: int = 200, exploration_weight: float = math.sqrt(2.0), rollout_depth: int = 20):
        super().__init__(game)
        self.iterations = iterations
        self.exploration_weight = exploration_weight
        self.rollout_depth = rollout_depth

    def _select_child(self, node: Vertex) -> Vertex:
        log_parent_visits = math.log(node.visits) if node.visits > 0 else 0.0
        best_score = float("-inf")
        best_child = node.children[0]

        for child in node.children:
            if child.visits == 0:
                score = float("inf")
            else:
                exploitation = child.total_reward / child.visits
                exploration = self.exploration_weight * math.sqrt(log_parent_visits / child.visits)
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def _expand(self, node: Vertex) -> Vertex:
        if not node.untried_moves:
            raise ValueError("Aucun coup disponible à développer.")

        move = node.untried_moves.pop()
        next_state = copy.deepcopy(node.state)
        current_player = next_state.current_player

        if current_player is None:
            raise ValueError("Aucun joueur courant pour développer le nœud.")

        next_state.play_move(current_player, move)
        next_state.set_game_state()
        next_state._current_player = next_state.opponent(current_player)

        child = Vertex(state=next_state, parent=node, move=move)
        node.add_child(child)
        return child

    def _evaluate_terminal_state(self, state, root_player):
        if state._game_state == GameState.DRAW:
            return 0.5

        if state._game_state == GameState.CURRENT_WIN:
            winner = state.current_player
        elif state._game_state == GameState.OPPONENT_WIN:
            winner = state.opponent(state.current_player)
        else:
            return 0.5

        return 1.0 if winner == root_player else 0.0

    def _rollout(self, state, root_player):
        current_state = copy.deepcopy(state)
        current_player = current_state.current_player

        for _ in range(self.rollout_depth):
            if current_state._game_state != GameState.ONGOING:
                break

            possible_moves = current_state.possible_moves(current_player.position)
            if not possible_moves:
                current_state.set_game_state()
                break

            move = random.choice(possible_moves)
            current_state.play_move(current_player, move)
            current_state.set_game_state()
            current_player = current_state.opponent(current_player)

        return self._evaluate_terminal_state(current_state, root_player)

    def _backpropagate(self, node: Vertex, result: float) -> None:
        current = node
        while current is not None:
            current.visits += 1
            current.total_reward += result
            current = current.parent

    def get_move(self, from_position: tuple[int, int], other_player_position: tuple[int, int]) -> tuple[int, int] | None:
        if self.game is None:
            return None

        state = copy.deepcopy(self.game)

        if state.player_1 is not None and state.player_1.position == from_position:
            root_player = state.player_1
        elif state.player_2 is not None and state.player_2.position == from_position:
            root_player = state.player_2
        else:
            root_player = state.current_player

        if root_player is None:
            return None
        if state.player_1 is not None and state.player_2 is not None:
            other_player = state.player_1 if root_player == state.player_2 else state.player_2
            if other_player is not None:
                other_player_position = other_player.position

        root = Vertex(state=state)
        root.state._current_player = root_player

        if not root.untried_moves:
            return None

        for _ in range(self.iterations):
            node = root

            while not node.untried_moves and node.children and not node.is_terminal:
                node = self._select_child(node)

            if not node.is_terminal and node.untried_moves:
                node = self._expand(node)

            result = self._rollout(node.state, root_player)
            self._backpropagate(node, result)

        if not root.children:
            return root.untried_moves[0] if root.untried_moves else None

        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.move

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.MCTS
