import pygame

from src.classes.algorithms.human import Human
from src.classes.algorithms.stupidbot import StupidBot
from src.classes.player import Player
from src.classes.manic_mine_layers import ManicMineLayers
from src.schemas.cell_state import CellState

class GameView:
    def __init__(self, manic_mine_layers: ManicMineLayers, case_size: int=60):
        pygame.init()

        self.manic_mine_layers = manic_mine_layers
        self.case_size = case_size

        width = self.manic_mine_layers.column_length * self.case_size
        height = self.manic_mine_layers.row_length * self.case_size + 40

        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Manic Minelayers")

    def display(self):
        """
        Show the grid 
        """
        self.screen.fill((255, 255, 255))

        for i in range(len(self.manic_mine_layers.grid)):
            for j in range(len(self.manic_mine_layers.grid[i])):
                rectangle = pygame.Rect(j * self.case_size, i * self.case_size, self.case_size, self.case_size)
                value = self.manic_mine_layers.grid[i][j]

                if  value == CellState.PLAYER1:
                    pygame.draw.circle(self.screen, (220, 50, 50), rectangle.center, self.case_size // 3)
                elif value == CellState.PLAYER2:
                    pygame.draw.circle(self.screen, (50, 80, 220), rectangle.center, self.case_size // 3)
                elif value == CellState.MARKED:
                    pygame.draw.line(self.screen, (220, 50, 50), rectangle.topleft, rectangle.bottomright, 5)                       
                    pygame.draw.line(self.screen, (220, 50, 50), rectangle.topright, rectangle.bottomleft, 5)   

                pygame.draw.rect(self.screen, (0, 0, 0), rectangle, 1)

        text_surface = self.font.render(f"Au tour du joueur {"1" if self.manic_mine_layers.current_player == self.manic_mine_layers.player_1 else "2"}", True, (0, 0, 0))
        center_x = (self.manic_mine_layers.column_length * self.case_size) // 2
        center_y = self.manic_mine_layers.row_length * self.case_size + 20
        text_center = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_center)        
        pygame.display.flip()

    def pixel_to_cell(self, x, y):
        """
        Convert pixels (x,y) to (i,j)
        """
        i = y // self.case_size 
        j = x // self.case_size
        if 0 <= i < self.manic_mine_layers.row_length and 0 <= j < self.manic_mine_layers.column_length:
            return i,j
        return None

    def choose_cell(self) -> None | tuple[int, int]:
        """
        Choose a cell by clicking a cell on the screen

        returns None or tuple[int, int]. If None, it means a human player decided to stop the game.
        """
        cell: tuple[int, int] | None = None
        in_game = True
        while in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    cell = self.pixel_to_cell(x,y)
                    return cell
        pygame.quit()  
        return cell

if __name__ == "__main__":
    # Use only for dev tests. Unit tests will be added then.
    game = ManicMineLayers()
    game.set_players(
        current_player=1,
        player_1=Player(
            algorithm=Human(game=game),
            number=1
        ),
        player_2=Player(
            algorithm=StupidBot(game=game),
            number=2
        )
    )
    view = GameView(game)
    game.start(view)
