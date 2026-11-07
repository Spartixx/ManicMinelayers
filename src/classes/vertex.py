from typing import Any

from src.schemas.game_state import GameState


class Vertex:


    def __init__(self, state: Any, parent: "Vertex | None" = None, move: tuple[int, int] | None = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children: list[Vertex] = []
        self.untried_moves: list[tuple[int, int]] = self._get_available_moves()
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

    def add_child(self, child: "Vertex") -> None:
        self.children.append(child)

    def __repr__(self) -> str:
        return f"Vertex(move={self.move}, visits={self.visits}, reward={self.total_reward}, children={len(self.children)})"
