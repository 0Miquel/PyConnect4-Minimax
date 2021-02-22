import pygame

pygame.init()


image_board = pygame.image.load('./images/board.png')
image_yellow = pygame.image.load('./images/yellow.png')
image_red = pygame.image.load('./images/red.png')


DIM_SQUARE = 67

N_ROWS = 7
N_COLS = 8

SCREEN_X = DIM_SQUARE * N_COLS
SCREEN_Y = DIM_SQUARE * N_ROWS

WINDOW_SIZE = 4

EMPTY = 0
AI_PLAYER = 2
OPP_PLAYER = 1

