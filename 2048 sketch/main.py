import pygame
import random
import sys

# Dimensions de la grille
GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 10
WIDTH = GRID_SIZE * (CELL_SIZE + MARGIN) + MARGIN
HEIGHT = GRID_SIZE * (CELL_SIZE + MARGIN) + MARGIN

# Couleurs
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 119),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 204, 97),
    256: (237, 200, 80),
    512: (237, 196, 63),
    1024: (237, 194, 46),
    2048: (237, 192, 38),
}

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")
font = pygame.font.SysFont("Arial", 32)

# Initialisation de la grille
def new_game():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_number(grid)
    add_new_number(grid)
    return grid

def add_new_number(grid):
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = random.choice([2, 4])

def draw_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            x = col * (CELL_SIZE + MARGIN) + MARGIN
            y = row * (CELL_SIZE + MARGIN) + MARGIN
            pygame.draw.rect(screen, CELL_COLORS.get(value, BACKGROUND_COLOR), (x, y, CELL_SIZE, CELL_SIZE))
            if value != 0:
                text = font.render(str(value), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + CELL_SIZE / 2, y + CELL_SIZE / 2))
                screen.blit(text, text_rect)

def move_left(grid):
    changed = False
    for row in range(GRID_SIZE):
        new_row = [x for x in grid[row] if x != 0]
        new_row = merge(new_row)
        new_row += [0] * (GRID_SIZE - len(new_row))
        if new_row != grid[row]:
            changed = True
        grid[row] = new_row
    return changed

def merge(row):
    for i in range(1, len(row)):
        if row[i] == row[i - 1] and row[i] != 0:
            row[i - 1] *= 2
            row[i] = 0
    return [x for x in row if x != 0]

def move_right(grid):
    grid = [list(reversed(row)) for row in grid]
    changed = move_left(grid)
    return [list(reversed(row)) for row in grid], changed

def move_up(grid):
    grid = list(zip(*grid))
    grid, changed = move_left(grid)
    return [list(row) for row in zip(*grid)], changed

def move_down(grid):
    grid = list(zip(*grid))
    grid, changed = move_right(grid)
    return [list(row) for row in zip(*grid)], changed

def check_game_over(grid):
    for row in grid:
        if 2048 in row:
            return "You win!"
    if all(grid[r][c] != 0 for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
        return "Game over!"
    return None

def main():
    grid = new_game()

    run_ended = False
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if run_ended:
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if move_left(grid):
                        add_new_number(grid)
                elif event.key == pygame.K_RIGHT:
                    grid, changed = move_right(grid)
                    if changed:
                        add_new_number(grid)
                elif event.key == pygame.K_UP:
                    grid, changed = move_up(grid)
                    if changed:
                        add_new_number(grid)
                elif event.key == pygame.K_DOWN:
                    grid, changed = move_down(grid)
                    if changed:
                        add_new_number(grid)

        screen.fill(BACKGROUND_COLOR)
        # Dessine grille et les cases
        draw_grid(grid)
        # Vérifier la fin du jeu
        message = check_game_over(grid)
        if message:
            run_ended = True
            game_over_text = font.render(message, True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(game_over_text, text_rect)
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
