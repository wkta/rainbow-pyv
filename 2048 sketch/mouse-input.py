# NOT USED, just yet

import pygame

# Dimensions de la grille
GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 10
WIDTH = GRID_SIZE * (CELL_SIZE + MARGIN) + MARGIN
HEIGHT = GRID_SIZE * (CELL_SIZE + MARGIN) + MARGIN

# Dimensions des boutons (flèches)
BUTTON_WIDTH = 60
BUTTON_HEIGHT = 60
BUTTON_MARGIN = 20

# Définitions des zones cliquables pour les flèches
ARROW_LEFT = pygame.Rect(BUTTON_MARGIN, HEIGHT - BUTTON_MARGIN - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
ARROW_RIGHT = pygame.Rect(WIDTH - BUTTON_MARGIN - BUTTON_WIDTH, HEIGHT - BUTTON_MARGIN - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
ARROW_UP = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
ARROW_DOWN = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_MARGIN - BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT)

# Fonction pour dessiner les flèches
def draw_arrows(screen):
    pygame.draw.rect(screen, (255, 0, 0), ARROW_LEFT)
    pygame.draw.rect(screen, (255, 0, 0), ARROW_RIGHT)
    pygame.draw.rect(screen, (255, 0, 0), ARROW_UP)
    pygame.draw.rect(screen, (255, 0, 0), ARROW_DOWN)

    font = pygame.font.SysFont("Arial", 32)
    left_text = font.render("<", True, (255, 255, 255))
    right_text = font.render(">", True, (255, 255, 255))
    up_text = font.render("^", True, (255, 255, 255))
    down_text = font.render("v", True, (255, 255, 255))

    screen.blit(left_text, (ARROW_LEFT.centerx - left_text.get_width() / 2, ARROW_LEFT.centery - left_text.get_height() / 2))
    screen.blit(right_text, (ARROW_RIGHT.centerx - right_text.get_width() / 2, ARROW_RIGHT.centery - right_text.get_height() / 2))
    screen.blit(up_text, (ARROW_UP.centerx - up_text.get_width() / 2, ARROW_UP.centery - up_text.get_height() / 2))
    screen.blit(down_text, (ARROW_DOWN.centerx - down_text.get_width() / 2, ARROW_DOWN.centery - down_text.get_height() / 2))

# Fonction pour détecter les clics de souris et savoir si l'utilisateur a cliqué sur une flèche
def detect_arrow_clicks(mouse_pos):
    if ARROW_LEFT.collidepoint(mouse_pos):
        return 'LEFT'
    if ARROW_RIGHT.collidepoint(mouse_pos):
        return 'RIGHT'
    if ARROW_UP.collidepoint(mouse_pos):
        return 'UP'
    if ARROW_DOWN.collidepoint(mouse_pos):
        return 'DOWN'
    return None
