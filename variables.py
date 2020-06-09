board = [None,None,None,
         None,None,None,
         None,None,None]

run = True

screen_width = 700
screen_height = 400

cell_x = 220
cell_y1=105
cell_y2=183
cell_y3=261
cell_diff = 90
cell_width = 77
cell_height = 65

cell_color = (21,189,172)
bg_color = (21,189,172)
white = (255,255,255)
score_color = (130,130,130)

player_pos = {0:(255,138),1:(344,138),2:(433,138),3:(255,215),4:(344,215),5:(433,215),6:(255,294),7:(344,294),8:(433,294)}

score_x = 0
score_o = 0

is_menu = False
m_option_1 = None
m_option_2 = None

turn = 1
k = 0
winner = None

chosen_gameState = None

restart_button = None
menu_button = None
human_button = None
comp_button = None

gameState = 0      #0 - Start Screen    1 - 1-on-1    2 - Comp   3 - x_wins    4 - o_wins   5 - tie
