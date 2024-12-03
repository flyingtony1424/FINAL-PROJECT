import random

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.solution = None

    def get_board(self):
        return self.board

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 3)
        self.solution = [row[:] for row in self.board]
        self.remove_cells()

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_box(self, row_start, col_start):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = numbers.pop()

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[i][col] for i in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (
            self.valid_in_row(row, num)
            and self.valid_in_col(col, num)
            and self.valid_in_box(row - row % 3, col - col % 3, num)
        )

    def fill_remaining(self, i, j):
        if i == self.row_length - 1 and j == self.row_length:
            return True
        if j == self.row_length:
            i += 1
            j = 0
        if self.board[i][j] != 0:
            return self.fill_remaining(i, j + 1)

        for num in range(1, 10):
            if self.is_valid(i, j, num):
                self.board[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0

        return False

    def remove_cells(self):
        count = self.removed_cells
        while count > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1

def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    generator.fill_values()
    return generator.get_board()