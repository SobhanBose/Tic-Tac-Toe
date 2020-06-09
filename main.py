import pygame
pygame.init()

from math import inf as infinity
import time
import random

from variables import *

win=pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption("TIC - TAC - TOE")

cell=[None]*9
cross=pygame.image.load("cross.png")
dot=pygame.image.load("dot.png")
bg=pygame.image.load("background_1.png").convert()
start_screen=pygame.image.load("Start_Screen.png").convert()
o_turn=pygame.image.load("o_turn.png")
o_wins_screen=pygame.image.load("o_winner.png")
x_turn=pygame.image.load("x_turn.png")
x_wins_screen=pygame.image.load("x_winner.png")
game_over=pygame.image.load("draw_back.png")
tie_screen=pygame.image.load("Draw_screen.png")
menu=pygame.image.load("menu.png")
menu_cover=pygame.image.load("menu_cover.png")


def draw_Start_Screen():
    global human_button,comp_button,gameState,cells,chosen_gameState
    win.blit(start_screen,(0,0))
    human_button = pygame.draw.rect(win,bg_color,(271,201,198,32))
    comp_button = pygame.draw.rect(win,bg_color,(181,264,356,32))
    font = pygame.font.SysFont("freesansbold.ttf",40)
    button_text_display("Play 1-on-1",white,293,205,font,None)
    button_text_display("Play Against Computer",white,207,267,font,None)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if human_button.collidepoint(pygame.mouse.get_pos()):
                chosen_gameState = 1
                reset_variables()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if comp_button.collidepoint(pygame.mouse.get_pos()):
                chosen_gameState = 2
                reset_variables()
    
    
def reset_variables():
    global gameState,player,move,winner,board,cells,k,turn,result
    gameState = chosen_gameState
    win.blit(bg, (0,0))
    drawCells(cell_x,cell_y1,cell_y2,cell_y3,cell_color,cell_width,cell_height)
    draw_misc()
    pygame.display.update()
    board = [None,None,None,
             None,None,None,
             None,None,None]
    turn = 1
    k = 0
    player = "X"
    winner = None
    turn = 1
    move = None
    result = None

def drawCells(cell_x,cell_y1,cell_y2,cell_y3,cell_color,cell_width,cell_height):
    for i in range(0,3):
        cell[i] = pygame.draw.rect(win,cell_color,(cell_x,cell_y1,cell_width,cell_height))
        cell_x+=cell_diff
    cell_x = 220
    for i in range(3,6):
        cell[i] = pygame.draw.rect(win,cell_color,(cell_x,cell_y2,cell_width,cell_height))
        cell_x+=cell_diff
    cell_x=220
    for i in range(6,9):
        cell[i] = pygame.draw.rect(win,cell_color,(cell_x,cell_y3,cell_width,cell_height))
        cell_x+=cell_diff
    
def human_gameplay():
    global turn,cell,k,is_menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            pos = pygame.mouse.get_pos()
            print(pos)
            for i in range(9):
                if cell[i].collidepoint(pygame.mouse.get_pos()) and board[i]==None:
                    if turn == 1:
                        board[i] = "X"
                        player = "O"
                        drawCross(i)
                    elif turn == -1:
                        board[i] = "O"
                        player = "X"
                        drawDot(i)
                    turn*=-1
                    k+=1
                    print(board)
            if restart_button.collidepoint(pygame.mouse.get_pos()):
                reset_variables()
            if menu_button.collidepoint(pygame.mouse.get_pos()):
                interact_menu()

def comp_gameplay():
    global turn,cell,k,player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if turn == 1 and event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            pos = pygame.mouse.get_pos()
            print(pos)
            for i in range(9):
                    if cell[i].collidepoint(pos) and board[i]==None:
                        board[i] = player
                        drawCross(i)
                        turn*=-1
                        player = "O"
                        k+=1
                        print(board,"\n")
                        break
        elif turn == -1:
            move = compMove()
            time.sleep(1)
            board[move[0]] = player
            drawDot(move[0])
            turn*=-1
            player = "X"
            k+=1
            print(board)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if restart_button.collidepoint(pygame.mouse.get_pos()):
                reset_variables()
            if menu_button.collidepoint(pygame.mouse.get_pos()):
                interact_menu()

def availMoves(board):
    openMoves = [n for n in range(len(board)) if board[n] == None]
    return openMoves

def compMove():
    global winner
    depth = len(availMoves(board))
    print(k)
    if k==1 and (board[0] or board[2] or board[6] or board[8] == "X"):
        return [4,0]
    elif k==1 and (board[1] or board[3] or board[5] or board[7] == "X"):
        return [random.choice([0,2,6,8]),0]
    if depth == 0 or check_win(board)=="tie":
        return
    winner = None
    move = minimax(board, depth, "O")
    return move

def evaluate(board):
    check = check_win(board)
    if check == "O":
        score = 1
    elif check == "X":
        score = -1
    else:
        score = 0
    return score

def minimax(board,depth,player):
    global score,winner
    board_copy = board[:]
    if player == "O":
        best = [-1,-infinity]
    else:
        best = [-1,infinity]

    if depth == 0 or check_win(board_copy)=="tie":
        score = evaluate(board_copy)
        return [-1,score]
    winner = None
    
    for m in availMoves(board_copy):
        board_copy[m] = player
        if player == "O":
            score = minimax(board_copy,depth-1,"X")
        else:
            score = minimax(board_copy,depth-1,"O")
        board_copy[m] = None
        score[0] = m
        if player == "O":
            if best[1] < score[1]:
                best = score
        else:
            if best[1] > score[1]:
                best = score
    winner = None
    return best
        
def drawCross(i):
    cross_rect=cross.get_rect()
    cross_rect.center = player_pos[i]
    win.blit(cross,cross_rect)
    
def drawDot(i):
    dot_rect=dot.get_rect()
    dot_rect.center = player_pos[i]
    win.blit(dot,dot_rect)

def check_win(board):
    global winner
    for r in range(0,9,3):
        if(board[r] == board[r+1] == board[r+2] == "X"):
            winner = "X"
        elif(board[r] == board[r+1] == board[r+2] == "O"):
            winner = "O"
    for c in range(0,3):
        if(board[c] == board[c+3] == board[c+6] == "X"):
            winner = "X"
        elif(board[c] == board[c+3] == board[c+6] == "O"):
            winner = "O"
    if board[0] == board[4] == board[8] == "X":
        winner = "X"
    elif board[0] == board[4] == board[8] == "O":
        winner = "O"
    elif board[2] == board[4] == board[6] == "X":
        winner = "X"
    elif board[2] == board[4] == board[6] == "O":
        winner = "O"
    if k >= 9 and winner == None:
        winner = "tie"
    return winner

def changeScreen():
    if turn==1:
        win.blit(x_turn,(0,0))
    elif turn==-1:
        win.blit(o_turn,(0,0))

def button_text_display(msg,color,dis_x,dis_y,font,bgc):
    textSurf = font.render(msg,True,color,bgc) #None - white
    win.blit(textSurf,(dis_x,dis_y))
    
def draw_x_wins():
    global gameState,cell
    win.blit(game_over,(0,0))
    win.blit(x_wins_screen,(0,0))
    draw_restart_button()
    draw_misc()
    time.sleep(0.5)
    pygame.display.update()
    print("X Wins")
    while gameState!=chosen_gameState:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    reset_variables()
                if menu_button.collidepoint(pygame.mouse.get_pos()):
                    interact_menu()

def draw_o_wins():
    global gameState,cell
    win.blit(game_over,(0,0))
    win.blit(o_wins_screen,(0,0))
    draw_restart_button()
    draw_misc()
    time.sleep(0.5)
    pygame.display.update()
    print("O Wins")
    while gameState!=chosen_gameState:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    reset_variables()
                if menu_button.collidepoint(pygame.mouse.get_pos()):
                    interact_menu()
                        
def draw_tie():
    global gameState,cell
    win.blit(game_over,(0,0))
    win.blit(tie_screen, (0,0))
    draw_restart_button()
    draw_misc()
    time.sleep(0.5)
    pygame.display.update()
    print("It's a tie")
    while gameState!=chosen_gameState:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    reset_variables()
                if menu_button.collidepoint(pygame.mouse.get_pos()):
                    interact_menu()

def draw_restart_button():
    global restart_button
    restart_button = pygame.draw.rect(win,white,(48,348,611,24))

def draw_menu_button():
    global menu_button
    menu_button = pygame.draw.rect(win,bg_color,(0,146,9,125))

def interact_menu():
    global is_menu,gameState,chosen_gameState,score_x,score_o
    win.blit(menu,(0,0))
    is_menu = True
    m_option_1 = pygame.draw.rect(win,bg_color,(30,151,142,39))
    m_option_2 = pygame.draw.rect(win,bg_color,(30,228,142,39))
    font = pygame.font.SysFont("freesansbold.ttf",40)
    button_text_display("Play 1-on-1",white,30,157,font,None)
    font = pygame.font.SysFont("freesansbold.ttf",20)
    button_text_display("Play Against Computer",white,30,240,font,None)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                if menu_button.collidepoint(pygame.mouse.get_pos()):
                    win.blit(menu_cover,(0,0))
                    pygame.display.update()
                    is_menu = False
                if m_option_1.collidepoint(pygame.mouse.get_pos()):
                    chosen_gameState = 1
                    reset_variables()
                    is_menu = False
                if m_option_2.collidepoint(pygame.mouse.get_pos()):
                    chosen_gameState = 2
                    reset_variables()
                    is_menu = False
        if not(is_menu):
            score_x = score_o = 0
            break

def gameFlow():
    global score_x,score_o,gameState
    result = check_win(board)
    if result == "X":
        gameState = 3
        score_x+=1
    elif result == "O":
        gameState = 4
        score_o+=1
    elif result == "tie":
        gameState = 5
    else:
        changeScreen()
        draw_restart_button()
        draw_menu_button()
        draw_misc()
        if gameState == 1:
            human_gameplay()
        elif gameState == 2:
            comp_gameplay()
    pygame.display.update()
        
def draw_misc():
    font = pygame.font.SysFont("freesansbold.ttf",24)
    button_text_display("RESTART GAME",cell_color,280,353,font,white)
    font = pygame.font.SysFont("freesansbold.ttf",35)
    button_text_display(str(score_x),score_color,257,39,font,white)
    button_text_display(str(score_o),score_color,427,39,font,white)
    
#Driver Code
while run:
    if gameState == 0:
        draw_Start_Screen()
        pygame.display.update()
    elif gameState == 1 or gameState == 2:
        gameFlow()
    elif gameState == 3:
        draw_x_wins()
    elif gameState == 4:
        draw_o_wins()
    elif gameState == 5:
        draw_tie()
        

        

