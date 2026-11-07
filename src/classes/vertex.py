import copy
import math
from typing import Any

from src.schemas.game_state import GameState


class Vertex:
    def __init__(self, state: Any, parent: "Vertex | None" = None, move: tuple[int, int] | None = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children: list[Vertex] = []
        self.untried_moves = self._get_available_moves()
        self.visits = 0
        self.total_reward = 0.0

    def _get_available_moves(self) -> list[tuple[int, int]]:
        if self.state is None:
            return []

        current_player = getattr(self.state, "current_player", None)
        if current_player is None:
            return []

        possible_moves = getattr(self.state, "possible_moves", None)
        if not callable(possible_moves):
            return []

        return list(possible_moves(current_player.position))

    @property
    def is_terminal(self) -> bool:
        current_state = getattr(self.state, "_game_state", None)
        return current_state is not None and current_state != GameState.ONGOING

    def expand(self) -> "Vertex":
        if not self.untried_moves:
            raise ValueError("Aucun coup disponible à développer.")

        move = self.untried_moves.pop()
        next_state = copy.deepcopy(self.state)
        current_player = next_state.current_player

        if current_player is None:
            raise ValueError("Aucun joueur courant pour développer le nœud.")

        next_state.play_move(current_player, move)
        next_state.set_game_state()
        next_state._current_player = next_state.opponent(current_player)

        child = Vertex(state=next_state, parent=self, move=move)
        self.children.append(child)
        return child

    def select_child(self, exploration_weight: float = math.sqrt(2.0)) -> "Vertex":
        if not self.children:
            raise ValueError("Aucun enfant disponible pour la sélection.")

        log_parent_visits = math.log(self.visits) if self.visits > 0 else 0.0
        best_score = float("-inf")
        best_child = self.children[0]

        for child in self.children:
            if child.visits == 0:
                score = float("inf")
            else:
                exploitation = child.total_reward / child.visits
                exploration = exploration_weight * math.sqrt(log_parent_visits / child.visits)
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def backpropagate(self, reward: float) -> None:

        current = self
        while current is not None:
            current.visits += 1
            current.total_reward += reward
            current = current.parent

    def best_move(self) -> tuple[int, int] | None:
        if not self.children:
            return None

        return max(self.children, key=lambda child: child.visits).move

    def __repr__(self) -> str:
        return (
            f"Vertex(move={self.move}, visits={self.visits}, "
            f"reward={self.total_reward}, children={len(self.children)})"
        )
