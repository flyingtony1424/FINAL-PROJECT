import pygame
from board import Board

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 450
screen_height = 550  # Added extra height for buttons
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Game variables
running = True
game_started = False
difficulty = None
board = None

# Font
font = pygame.font.Font(None, 36)


def draw_start_screen():
    screen.fill(white)
    title_text = font.render("Sudoku", True, black)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)

    # Difficulty buttons
    easy_button = pygame.Rect(screen_width // 4, screen_height // 2, screen_width // 2, 50)
    pygame.draw.rect(screen, (150, 150, 150), easy_button)
    easy_text = font.render("Easy", True, black)
    easy_rect = easy_text.get_rect(center=easy_button.center)
    screen.blit(easy_text, easy_rect)

    medium_button = pygame.Rect(screen_width // 4, screen_height // 2 + 60, screen_width // 2, 50)
    pygame.draw.rect(screen, (150, 150, 150), medium_button)
    medium_text = font.render("Medium", True, black)
    medium_rect = medium_text.get_rect(center=medium_button.center)
    screen.blit(medium_text, medium_rect)

    hard_button = pygame.Rect(screen_width // 4, screen_height // 2 + 120, screen_width // 2, 50)
    pygame.draw.rect(screen, (150, 150, 150), hard_button)
    hard_text = font.render("Hard", True, black)
    hard_rect = hard_text.get_rect(center=hard_button.center)
    screen.blit(hard_text, hard_rect)

    pygame.display.update()


def draw_game_screen():
    screen.fill(white)
    board.draw()

    reset_button = pygame.Rect(screen_width // 6, screen_height - 100, screen_width // 3, 40)
    restart_button = pygame.Rect(screen_width * 3 // 6, screen_height - 100, screen_width // 3, 40)
    exit_button = pygame.Rect(screen_width // 6, screen_height - 50, screen_width * 2 // 3, 40)

    pygame.draw.rect(screen, black, reset_button, 2)
    pygame.draw.rect(screen, black, restart_button, 2)
    pygame.draw.rect(screen, black, exit_button, 2)

    reset_text = font.render("Reset", True, black)
    reset_rect = reset_text.get_rect(center=reset_button.center)
    screen.blit(reset_text, reset_rect)

    restart_text = font.render("Restart", True, black)
    restart_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_rect)

    exit_text = font.render("Exit", True, black)
    exit_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_rect)

    pygame.display.update()


def draw_game_over_screen(message):
    screen.fill(white)
    game_over_text = font.render(message, True, black)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)

    exit_button = pygame.Rect(screen_width // 6, screen_height // 2 + 40, screen_width * 2 // 3, 50)
    pygame.draw.rect(screen, black, exit_button, 2)
    exit_text = font.render("Exit", True, black)
    exit_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_rect)

    pygame.display.update()
    return exit_button


def handle_click(x, y):
    global game_started, difficulty, board

    if screen_width // 4 <= x <= screen_width * 3 // 4:
        if screen_height // 2 <= y <= screen_height // 2 + 50:
            difficulty = 30  # Easy
        elif screen_height // 2 + 60 <= y <= screen_height // 2 + 110:
            difficulty = 40  # Medium
        elif screen_height // 2 + 120 <= y <= screen_height // 2 + 170:
            difficulty = 50  # Hard

        if difficulty:
            game_started = True
            board = Board(screen_width, screen_height - 100, screen, difficulty)  # Adjust board height


def check_button_click(x, y, exit_button):
    global running, game_started, difficulty
    if screen_width // 6 <= x <= screen_width // 2 and screen_height - 100 <= y <= screen_height - 60:  # Reset
        board.reset_to_original()
    elif screen_width * 3 // 6 <= x <= screen_width * 5 // 6 and screen_height - 100 <= y <= screen_height - 60:  # Restart
        game_started = False
        difficulty = None
    elif screen_width // 6 <= x <= screen_width * 5 // 6 and screen_height - 50 <= y <= screen_height - 10:  # Exit
        running = False

    if exit_button and exit_button.collidepoint(x, y):
        running = False


# Game loop
exit_button = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not game_started:
                handle_click(x, y)
            elif board and board.is_won():
                check_button_click(x, y, exit_button)
            else:
                clicked_cell = board.click(x, y)
                if clicked_cell:
                    board.select(*clicked_cell)
                else:
                    check_button_click(x, y, None)
        elif event.type == pygame.KEYDOWN:
            if game_started and board.selected_cell:
                if event.key == pygame.K_1:
                    board.sketch(1)
                elif event.key == pygame.K_2:
                    board.sketch(2)
                elif event.key == pygame.K_3:
                    board.sketch(3)
                elif event.key == pygame.K_4:
                    board.sketch(4)
                elif event.key == pygame.K_5:
                    board.sketch(5)
                elif event.key == pygame.K_6:
                    board.sketch(6)
                elif event.key == pygame.K_7:
                    board.sketch(7)
                elif event.key == pygame.K_8:
                    board.sketch(8)
                elif event.key == pygame.K_9:
                    board.sketch(9)
                elif event.key == pygame.K_RETURN:
                    if board.selected_cell:
                        row, col = board.selected_cell
                        sketched_value = board.board[row][col].sketched_value
                        if sketched_value != 0:
                            board.place_number(sketched_value)
                            if board.is_won():
                                exit_button = draw_game_over_screen("You Win!")
                            elif board.is_full() and not board.is_won():
                                exit_button = draw_game_over_screen("Game Over!")

    if not game_started:
        draw_start_screen()
    else:
        screen.fill(white)
        draw_game_screen()

pygame.quit()