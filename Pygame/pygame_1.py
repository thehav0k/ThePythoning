## Tic Tac Toe Game in Pygame

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # Hide the pygame welcome message
import pygame
import sys

pygame.init()
# Global constants
WIDTH, HEIGHT = 300, 350
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER = (170, 170, 170)

# Initialize Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)

board = [[None]*BOARD_COLS for _ in range(BOARD_ROWS)]

def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, SQUARE_SIZE * BOARD_ROWS), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def check_win(player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    if all([board[i][i] == player for i in range(BOARD_ROWS)]):
        return True
    if all([board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True
    return False

def check_draw():
    return all(all(cell is not None for cell in row) for row in board)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

def draw_status(message):
    pygame.draw.rect(screen, BG_COLOR, (0, HEIGHT-50, WIDTH, 50))
    text = font.render(message, True, TEXT_COLOR)
    screen.blit(text, (10, HEIGHT-45))

def draw_buttons():
    play_rect = pygame.Rect(30, HEIGHT-45, 100, 35)
    exit_rect = pygame.Rect(170, HEIGHT-45, 100, 35)
    mouse = pygame.mouse.get_pos()
    for rect, label in [(play_rect, "Play Again"), (exit_rect, "Exit")]:
        color = BUTTON_HOVER if rect.collidepoint(mouse) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        text = small_font.render(label, True, TEXT_COLOR)
        screen.blit(text, (rect.x + 10, rect.y + 5))
    return play_rect, exit_rect

draw_lines()
player = 'X'
game_over = False
winner = None

while True:
    screen.fill(BG_COLOR, (0, SQUARE_SIZE*BOARD_ROWS, WIDTH, HEIGHT - SQUARE_SIZE*BOARD_ROWS))
    draw_lines()
    draw_figures()
    if not game_over:
        draw_status(f"{player}'s turn")
    else:
        if winner:
            draw_status(f"{winner} wins!")
        else:
            draw_status("It's a draw!")
        play_rect, exit_rect = draw_buttons()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < SQUARE_SIZE * BOARD_ROWS:
                    col = x // SQUARE_SIZE
                    row = y // SQUARE_SIZE
                    if board[row][col] is None:
                        board[row][col] = player
                        if check_win(player):
                            game_over = True
                            winner = player
                        elif check_draw():
                            game_over = True
                            winner = None
                        else:
                            player = 'O' if player == 'X' else 'X'
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                play_rect, exit_rect = draw_buttons()
                if play_rect.collidepoint((x, y)):
                    restart()
                    player = 'X'
                    game_over = False
                    winner = None
                elif exit_rect.collidepoint((x, y)):
                    pygame.quit()
                    sys.exit()

# Absolute Cinema
# I love this Library
# Huge Libray ! Gonna learn all later