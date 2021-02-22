import numpy as np
import pygame
from constants import *
import random
import math

pygame.init()

#modifiy board depending on your move
def mod_board(board, col, player,screen):
    can_move = False
    row = -5 # random value in case we return row before assignment
    
    if player == OPP_PLAYER:
        image_token = image_yellow
    else:
        image_token = image_red
    
    if col in get_valid_locations(board):
        can_move = True
        row = get_next_open_row(board[:,col])
        board[row][col] = player
        screen.blit(image_token, (col*DIM_SQUARE,row*DIM_SQUARE))
        
    return can_move, row, col

def is_win(board, player):
    #score horizontal
    for r in range(N_ROWS):
        row_array = list(board[r,:])
        for c in range(N_COLS-3):
            window = row_array[c:c+WINDOW_SIZE]
            if window.count(player) == len(window):
                return True
                
    #score vertical
    for c in range(N_COLS):
        col_array = list(board[:,c])
        for r in range(N_ROWS-3):
            window = col_array[r:r+WINDOW_SIZE]
            if window.count(player) == len(window):
                return True
                
    #score diagonal
    for r in range(N_ROWS-3):
        for c in range(N_COLS-3):
            window = [board[r+i][c+i] for i in range(WINDOW_SIZE)]
            if window.count(player) == len(window):
                return True
    for r in range(N_ROWS-3):
        for c in range(N_COLS-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_SIZE)]
            if window.count(player) == len(window):
                return True
            
    return False
    
def change_turn(player):
    if player == OPP_PLAYER:
        player = AI_PLAYER
    else:
        player = OPP_PLAYER
    return player
    

#check if the picked location is valid, so you can move or try again
def is_valid_location(board, col):
    n_zeros = np.count_nonzero(board[:,col] == 0)
    return n_zeros != 0

#get valid locations where you can move
def get_valid_locations(board):
    valid_locations = [i for i in range(N_COLS) if is_valid_location(board, i)]
    return valid_locations

#returns next open row where you can move
def get_next_open_row(entire_col):
    if np.where(entire_col != 0)[0].size != 0:
        row = np.where(entire_col != 0)[0][0] - 1
    else:
        row = N_ROWS-1
    return row
            
#pick best move possible
def pick_best_move(board, player):
    best_score = 0
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board[:,col])
        temp_board= board.copy()
        temp_board[row][col] = player

        new_score = get_score(temp_board, player)
        if new_score > best_score:
            best_score = new_score
            best_col = col
            
    return best_col
      
#evaluate each line so we know the total score of that move    
def get_score(board, player):
    score = 0
    
    center_array = list(board[:, N_COLS//2])
    score += center_array.count(player) * 6
    
    #score horizontal
    for r in range(N_ROWS):
        row_array = list(board[r,:])
        for c in range(N_COLS-3):
            window = row_array[c:c+WINDOW_SIZE]
            score += evaluate_window(window, player)
                
    #score vertical
    for c in range(N_COLS):
        col_array = list(board[:,c])
        for r in range(N_ROWS-3):
            window = col_array[r:r+WINDOW_SIZE]
            score += evaluate_window(window, player)
                
    #score diagonal
    for r in range(N_ROWS-3):
        for c in range(N_COLS-3):
            window = [board[r+i][c+i] for i in range(WINDOW_SIZE)]
            score += evaluate_window(window, player)
    for r in range(N_ROWS-3):
        for c in range(N_COLS-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_SIZE)]
            score += evaluate_window(window, player)
    
    return score

#evaluate window so as to know how worth is that move
def evaluate_window(window, player):
    score = 0
    opp_player = OPP_PLAYER
    if player == OPP_PLAYER:
        opp_player = AI_PLAYER
    
    if window.count(player) == 4:
        score += 1000
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2
    elif window.count(opp_player) == 3 and window.count(EMPTY) == 1:
        score -= 4
        
    return score

def is_terminal_node(board):
    return is_win(board, AI_PLAYER) or is_win(board, OPP_PLAYER) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if is_win(board, AI_PLAYER):
				return (None, 100000000000000)
			elif is_win(board, OPP_PLAYER):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, get_score(board, AI_PLAYER))
	if maximizingPlayer: #AI PLAYER
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board[:,col])
			b_copy = board.copy()
			b_copy[row][col] = AI_PLAYER
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player, OPP PLAYER
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board[:,col])
			b_copy = board.copy()
			b_copy[row][col] = OPP_PLAYER
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value


"""
#check if there is any winner
def check_winner(board, row, col, player):
    lines = get_lines(board, row, col)
    return is_win(lines, player)

#returns the lines affected by your last move
def get_lines(board, row, col):
    diag1 = board.diagonal(col - row)
    diag2 = np.fliplr(board).diagonal((N_COLS-1-col) - row) #modify col
    entire_col = np.flip(board[:,col]) 
    entire_row = board[row,:]
    return [diag1, diag2, entire_col, entire_row]
    

def is_win(lines, player):
    points = 0
    for line in lines:
        if points != 4:
            points = 0
            for i in line:
                if i == player:
                    points += 1
                    if points == 4:
                        break
                else:
                    points = 0
        else:
            break
    return points == 4
"""
    
    
    
    
        