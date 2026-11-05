import pygame

from src.enums.cell_state import CellState

class GameView:
    def __init__(self, row_length=5, column_length=10, case_size=60):
        pygame.init()
        self.case_size = case_size
        self.rows = row_length
        self.cols = column_length

        width = column_length * self.case_size
        height = row_length * self.case_size + 40
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("Arial", 24)
        pygame.display.set_caption("Manic Minelayers")


    def display(self, grid, message):
        """
        Show the grid 
        """
        self.screen.fill((255, 255, 255))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                rectangle = pygame.Rect(j * self.case_size, i * self.case_size, self.case_size, self.case_size)
                value = grid[i][j]

                if  value == CellState.PLAYER1:
                    pygame.draw.circle(self.screen, (220, 50, 50), rectangle.center, self.case_size // 3)
                elif value == CellState.PLAYER2:
                    pygame.draw.circle(self.screen, (50, 80, 220), rectangle.center, self.case_size // 3)
                elif value == CellState.MARKED:
                    pygame.draw.line(self.screen, (220, 50, 50), rectangle.topleft, rectangle.bottomright, 5)                       
                    pygame.draw.line(self.screen, (220, 50, 50), rectangle.topright, rectangle.bottomleft, 5)   

                pygame.draw.rect(self.screen, (0, 0, 0), rectangle, 1)

        text_surface = self.font.render(message, True, (0, 0, 0))
        center_x = (self.cols * self.case_size) // 2
        center_y = self.rows * self.case_size + 20
        text_center = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_center)        
        pygame.display.flip()


    def pixel_to_cell(self, x, y):
        """
        Convert pixels (x,y) to (i,j)
        """
        i = y // self.case_size 
        j = x // self.case_size
        if 0 <= i < self.rows and 0 <= j < self.cols:
            return i,j
        return None
    def launch(self):
        in_game = True
        grid = [[CellState.EMPTY for _ in range(10)] for _ in range(5)]
        grid[2][5] = CellState.PLAYER1
        grid[1][3] = CellState.PLAYER2
        grid[0][0] = CellState.MARKED
        while in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    cell = self.pixel_to_cell(x,y)
                    print(cell)

            self.display(grid, "Au tour du joueur 1")
        pygame.quit()  


view = GameView()
view.launch()