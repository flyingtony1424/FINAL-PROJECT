from sudoku_generator import SudokuGenerator
import pygame
from cell import Cell

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cell_size = self.width // 9
        self.selected_cell = None
        self.board = self.create_board()
        self.original_board = [[cell.value for cell in row] for row in self.board]

    def create_board(self):
        generator = SudokuGenerator(9, self.difficulty)
        generator.fill_values()
        board_values = generator.get_board()
        return [[Cell(board_values[i][j], i, j, self.screen, self.cell_size) for j in range(9)] for i in range(9)]

    def reset_to_original(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                cell.set_cell_value(self.original_board[i][j])
                cell.is_correct = True
                cell.set_sketched_value(0)

    def check_board(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col].value == 0:
                    return False
                for i in range(9):
                    if i != col and self.board[row][i].value == self.board[row][col].value:
                        return False
                    if i != row and self.board[i][col].value == self.board[row][col].value:
                        return False
                box_row = (row // 3) * 3
                box_col = (col // 3) * 3
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        if self.board[i][j].value == self.board[row][col].value and (i, j) != (row, col):
                            return False
        return True

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def is_won(self):
        return self.is_full() and self.check_board()

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.board[row][col].value == 0:
                self.board[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.board[row][col].value == 0:
                self.board[row][col].set_cell_value(value)
                if not self.is_valid_placement(row, col, value):
                    self.board[row][col].is_correct = False
                else:
                    self.board[row][col].is_correct = True

    def is_valid_placement(self, row, col, value):
        for i in range(9):
            if i != col and self.board[row][i].value == value:
                return False
            if i != row and self.board[i][col].value == value:
                return False
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j].value == value and (i, j) != (row, col):
                    return False
        return True

    def draw(self):
        for row in self.board:
            for cell in row:
                cell.draw()

        for i in range(10):
            if i % 3 == 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size), (self.width, i * self.cell_size), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, self.height), thickness)

    def select(self, row, col):
        self.selected_cell = (row, col)

    def click(self, x, y):
        if 0 <= x <= self.width and 0 <= y <= self.height:
            row = y // self.cell_size
            col = x // self.cell_size
            return row, col
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.board[row][col].value == 0:
                self.board[row][col].set_sketched_value(0)