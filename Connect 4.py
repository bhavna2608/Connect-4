import numpy as np
import pygame
import sys
import math

BLUE = (49, 184, 224)
BLACK = (0, 0, 0)
PURPLE = (105, 55, 222)
GREEN = (71, 199, 32)
WHITE = (255, 255, 255)

game_over = False
row_count = int(input("Enter the number of rows you would like: "))
column_count = int(input("Enter the number of columns you would like: "))
if row_count < 4 and column_count < 4:
    print("At least one dimension should be greater than 4!!")
    game_over = True

ROW_COUNT = row_count
COLUMN_COUNT = column_count

def create_board(game_over):
    if game_over == False:
       board = np.zeros([ROW_COUNT,COLUMN_COUNT], dtype='int16')
    return board 

def drop_piece(board, row, column, piece):
    board[row][column] = piece
    
def is_valid(board, column):
    return board[0][column] == 0
    
def get_next_open_row(board, column, n):
    while n:
        if board[n][column] == 0:
           return n
        else:
           n=n-1
        
def winning_move(board, piece, COLUMN_COUNT, ROW_COUNT):
#Horizonal check
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if  board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
               return True
#Verical check
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
               return True
#Negative diagonal check
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
               return True
#Positive diagonal check 
    for c in range(3, COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c-1] == piece and board[r+2][c-2] == piece and board[r+3][c-3] == piece:
               return True
        
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLACK, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
              pygame.draw.circle(screen, PURPLE, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 1:
              pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
            else:
              pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board = create_board(game_over)
turn = 0
n = ROW_COUNT-1

pygame.init()

SQUARESIZE = 70

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont('comicsans', 75)

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn % 2 == 0:
                pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, GREEN, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
           pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
              #Ask Player 1 input
           if turn % 2 == 0:
              posx = event.pos[0]
              column = int(math.floor(posx/SQUARESIZE))
            
              if is_valid(board, column):
                    row = get_next_open_row(board, column, n)
                    drop_piece(board, row, column, 1)
                    
              turn += 1
            
              print(board)
              draw_board(board)
                
              if winning_move(board, 1, COLUMN_COUNT, ROW_COUNT):
                label = myfont.render("Player 1 won! Congrats!!", 1, WHITE)
                screen.blit(label, (40,10))
                game_over = True
                turn = 0
                
               #Ask Player 2 input
           else:
              posx = event.pos[0]
              column = int(math.floor(posx/SQUARESIZE))
              
              if is_valid(board, column):
                    row = get_next_open_row(board, column, n)
                    drop_piece(board, row, column, 2)
                    
              turn += 1
            
              print(board)
              draw_board(board)
                
              if winning_move(board, 2, COLUMN_COUNT, ROW_COUNT):
                label = myfont.render("Player 2 won! Congrats!!", 1, WHITE)
                pygame.display.update
                screen.blit(label, (40,10))
                game_over = True
              
              if game_over:
                pygame.time.wait(2500)