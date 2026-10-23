import pygame
import sys
from board import Board

# Constants for screen size and title
WIDTH, HEIGHT = 600, 700
TITLE = "Sudoku"

def __main__():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    board = None
    running = True
    game_state = "welcome"  # Can be "welcome", "playing", or "game_over"
    difficulty = None
    win = None  # Will be set to True if the user wins, False otherwise
    row = 0
    col = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if game_state == "welcome":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 100 <= pos[0] <= 180 and 400 <= pos[1] <= 440:  # Easy
                        difficulty = "easy"
                        game_state = "playing"
                        board = Board(WIDTH, WIDTH, screen, difficulty)
                        board.generate_board()
                    elif 200 <= pos[0] <= 330 and 400 <= pos[1] <= 440:  # Medium
                        difficulty = "medium"
                        game_state = "playing"
                        board = Board(WIDTH, WIDTH, screen, difficulty)
                        board.generate_board()
                    elif 350 <= pos[0] <= 432 and 400 <= pos[1] <= 440:  # Hard
                        difficulty = "hard"
                        game_state = "playing"
                        board = Board(WIDTH, WIDTH, screen, difficulty)
                        board.generate_board()

            elif game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 0 <= pos[0] < 600 and 0 <= pos[1] < 600:
                        row, col = int(pos[1] // (600 / 9)), int(pos[0] // (600 / 9))
                        board.select(row, col)
                        selected = True

                    # Check if user clicked on buttons
                    if 100 <= pos[0] <= 200 and 620 <= pos[1] <= 680:  # Reset button
                        board.reset_to_original()
                    elif 230 <= pos[0] <= 355 and 620 <= pos[1] <= 680:  # Restart button
                        game_state = "welcome"  # Reset to welcome screen
                        difficulty = None
                    elif 385 <= pos[0] <= 458 and 620 <= pos[1] <= 680:  # Quit button
                        running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in {pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                     pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9}:
                        # Sketch value
                        board.sketch(event.key - pygame.K_0)
                    elif event.key == pygame.K_RETURN:
                        # Lock value
                        if board.selected_cell and board.selected_cell.sketched_value != 0:
                            board.place_number(board.selected_cell.sketched_value)
                    elif event.key in {pygame.K_UP} and board.selected_cell:
                        row = max(0, row - 1)
                        board.select(row, col)
                    elif event.key in {pygame.K_DOWN} and board.selected_cell:
                        row = min(8, row + 1)
                        board.select(row, col)
                    elif event.key in {pygame.K_LEFT} and board.selected_cell:
                        col = max(0, col - 1)
                        board.select(row, col)
                    elif event.key in {pygame.K_RIGHT} and board.selected_cell:
                        col = min(8, col + 1)
                        board.select(row, col)

                # Check for win/loss conditions
                if board.is_full():
                    if board.check_board():
                        game_state = "game_over"
                        win = True
                    else:
                        game_state = "game_over"
                        win = False

            elif game_state == "game_over":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if win:  # Exit button on Game Won
                        if 230 <= pos[0] <= 355 and 400 <= pos[1] <= 460:
                            running = False
                    else:  # Restart button on Try Again
                        if 230 <= pos[0] <= 355 and 400 <= pos[1] <= 460:
                            game_state = "welcome"
                            difficulty = None

        screen.fill((255, 255, 255))  # Clear the screen with a white background

        if game_state == "welcome":
            # Draw the welcome screen
            font = pygame.font.Font(None, 60)
            sub_font = pygame.font.Font(None, 40)
            title = font.render("Welcome to Sudoku", True, (0, 0, 0))
            instruction = sub_font.render("Select a Difficulty", True, (0, 0, 0))
            screen.blit(title, (100, 200))
            screen.blit(instruction, (150, 300))

            # Draw difficulty buttons
            easy_button = pygame.Rect(100, 400, 80, 40)
            medium_button = pygame.Rect(200, 400, 130, 40)
            hard_button = pygame.Rect(350, 400, 82, 40)
            pygame.draw.rect(screen, (255, 0, 0), easy_button)
            pygame.draw.rect(screen, (255, 0, 0), medium_button)
            pygame.draw.rect(screen, (255, 0, 0), hard_button)

            # Draw difficulty text
            sub_font = pygame.font.Font(None, 30)
            easy_text = sub_font.render("Easy", True, (255, 255, 255))
            medium_text = sub_font.render("Medium", True, (255, 255, 255))
            hard_text = sub_font.render("Hard", True, (255, 255, 255))
            screen.blit(easy_text, (110, 405))
            screen.blit(medium_text, (210, 405))
            screen.blit(hard_text, (360, 405))

        elif game_state == "playing":
            # Draw the board
            board.draw()

            # Draw Reset, Restart, Quit buttons
            reset_box = pygame.Rect((100, 620), (100, 60))
            pygame.draw.rect(screen, (255, 0, 0), reset_box)
            restart_box = pygame.Rect((230, 620), (125, 60))
            pygame.draw.rect(screen, (255, 0, 0), restart_box)
            exit_box = pygame.Rect((385, 620), (73, 60))
            pygame.draw.rect(screen, (255, 0, 0), exit_box)

            options_font = pygame.font.Font(None, 50)

            # Add text for the options
            reset_text = options_font.render("Reset", 0, (255, 255, 255))
            screen.blit(reset_text, (102, 630))
            restart_text = options_font.render("Restart", 0, (255, 255, 255))
            screen.blit(restart_text, (232, 630))
            exit_text = options_font.render("Exit", 0, (255, 255, 255))
            screen.blit(exit_text, (387, 630))

        elif game_state == "game_over":
            # Display win or loss screen
            font = pygame.font.Font(None, 80)
            if win:
                message = font.render("You Won!", True, (0, 128, 0))
                screen.blit(message, (150, 250))

                # Exit button for Game Won
                exit_box = pygame.Rect((230, 400), (125, 60))
                pygame.draw.rect(screen, (255, 0, 0), exit_box)
                exit_font = pygame.font.Font(None, 50)
                exit_text = exit_font.render("Exit", True, (255, 255, 255))
                screen.blit(exit_text, (260, 410))
            else:
                message = font.render("Try Again!", True, (255, 0, 0))
                screen.blit(message, (150, 250))

                # Restart button for Game Over
                restart_box = pygame.Rect((230, 400), (150, 60))
                pygame.draw.rect(screen, (255, 0, 0), restart_box)
                restart_font = pygame.font.Font(None, 50)
                restart_text = restart_font.render("Restart", True, (255, 255, 255))
                screen.blit(restart_text, (245, 410))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    __main__()
