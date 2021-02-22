import pygame
from connect4 import *
from constants import *
import math

pygame.init()

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
screen.blit(image_board, (0,0))
pygame.display.set_caption('Conecta4')

running = True
end = False
board = np.zeros((N_ROWS,N_COLS))
player = OPP_PLAYER
play = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if player == OPP_PLAYER:
            if event.type == pygame.MOUSEBUTTONUP and end == False:
                x,y = pygame.mouse.get_pos()
                col = int(x/DIM_SQUARE)
                play = True
        elif end == False:
            col, minimax_score = minimax(board, 4,-math.inf, math.inf, True)
            play = True
            
        if play:
            can_move, row, col = mod_board(board, col, player,screen)
            if can_move:
                end = is_win(board, player)
                if end == False:
                    player = change_turn(player)
                else:
                    print("Player", player, "wins")
            play = False
                    
    pygame.display.update()
    
pygame.quit()


