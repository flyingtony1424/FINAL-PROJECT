import pygame

class Cell:
    def __init__(self, value, row, col, screen, cell_size=50):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.cell_size = cell_size
        self.selected = False
        self.is_correct = True  # Initial assumption that the cell value is correct
        self.font = pygame.font.Font(None, int(self.cell_size * 0.75))

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * self.cell_size
        y = self.row * self.cell_size

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 3)

        if self.value != 0:
            color = (0, 0, 0) if self.is_correct else (255, 0, 0)  # Black if correct, red if incorrect
            text_surface = self.font.render(str(self.value), True, color)
            text_rect = text_surface.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
            self.screen.blit(text_surface, text_rect)
        elif self.sketched_value != 0:
            text_surface = self.font.render(str(self.sketched_value), True, (128, 128, 128))
            text_rect = text_surface.get_rect(topleft=(x + 5, y + 5))
            self.screen.blit(text_surface, text_rect)