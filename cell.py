import pygame, sys

CELL_SIZE = 600 / 9
GRID_SIZE = 9
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
WIDTH = 600
HEIGHT = 700


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0  # Holds sketched value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.locked = value != 0  # Locked if the cell was part of the initial puzzle

    def set_cell_value(self, value):
        if not self.locked:  # Only allow setting if the cell is not locked
            self.value = value
            self.sketched_value = 0  # Clear sketched value

    def set_sketched_value(self, value):
        if not self.locked:  # Only allow sketching if the cell is not locked
            self.sketched_value = value

    def draw(self):
        # Render the cell
        rect = pygame.Rect(self.col * CELL_SIZE, self.row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED if self.selected else WHITE, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 1)  # Border

        # Render the value or sketched value
        font = pygame.font.Font(None, 40)
        if self.value != 0:  # Display locked value
            text = font.render(str(self.value), True, BLACK)
            self.screen.blit(text, (self.col * CELL_SIZE + 20, self.row * CELL_SIZE + 20))
        elif self.sketched_value != 0:  # Display sketched value
            text = font.render(str(self.sketched_value), True, ORANGE)
            self.screen.blit(text, (self.col * CELL_SIZE + 20, self.row * CELL_SIZE + 20))
