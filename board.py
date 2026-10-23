import pygame
import cell
from cell import Cell
from sudoku_generator import SudokuGenerator

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.grid = []
        self.original_grid = []
        self.selected_cell = None

    def generate_board(self):
        removed_cells = self.get_removed_cells()
        generator = SudokuGenerator(9, removed_cells)
        generator.fill_values()
        generator.remove_cells()
        board = generator.get_board()

        # Initialize the grid with Cell objects
        self.grid = [
            [Cell(board[i][j], i, j, self.screen) for j in range(9)]
            for i in range(9)
        ]
        self.original_grid = [row[:] for row in board]

    def get_removed_cells(self):
        if self.difficulty == "easy":
            return 30
        elif self.difficulty == "medium":
            return 40
        elif self.difficulty == "hard":
            return 50
        return 30

    def draw(self):
        # Draw the Sudoku grid
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (i * (600/9), 0), (i * (600/9), 600), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * (600/9)), (600, i * (600/9)), thickness)

        # Draw each cell
        for row in self.grid:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        # Mark the selected cell
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.grid[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        # Determine the cell based on mouse click
        if 0 <= x < 450 and 0 <= y < 450:
            col = x // 50
            row = y // 50
            self.select(row, col)
            return row, col
        return None

    def clear(self):
        # Clear the selected cell's value if it's not part of the original puzzle
        if self.selected_cell and self.original_grid[self.selected_cell.row][self.selected_cell.col] == 0:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        # Set a sketched value in the selected cell
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        # Lock the cell with the placed value
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.locked = True

    def reset_to_original(self):
        # Reset all cells to their original values and unlock them
        for i in range(9):
            for j in range(9):
                self.grid[i][j].set_cell_value(self.original_grid[i][j])  # Reset value
                self.grid[i][j].locked = self.original_grid[i][j] != 0  # Re-lock original non-zero cells
                self.grid[i][j].set_sketched_value(0)  # Clear any sketched values

    def is_full(self):
        # Check if all cells are filled
        return all(cell.value != 0 for row in self.grid for cell in row)

    def update_board(self):
        # Update the 2D array representation of the board from the Cell objects
        board = [[self.grid[i][j].value for j in range(9)] for i in range(9)]
        return board

    def find_empty(self):
        # Find the first empty cell
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].value == 0:
                    return i, j
        return None

    def check_board(self):
        # Check if the current board is a valid solution
        for i in range(9):
            row = [self.grid[i][j].value for j in range(9)]
            col = [self.grid[j][i].value for j in range(9)]
            if len(set(row)) != 9 or len(set(col)) != 9:
                return False
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [
                    self.grid[r][c].value
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                ]
                if len(set(box)) != 9:
                    return False
        return True

    def check_win(self):
        # Check if the board is full and correctly solved
        if self.is_full() and self.check_board():
            print("You won!")
            return True
        elif self.is_full():
            print("Board is full but incorrect!")
            return False
        return None


