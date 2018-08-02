# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos= [WIDTH/2,HEIGHT/2]
ball_vel=[1,-0.5]

paddle1_pos=[[0,0],[PAD_WIDTH,0],[PAD_WIDTH,PAD_HEIGHT],[0,PAD_HEIGHT]]
paddle2_pos=[[WIDTH,0],[WIDTH-PAD_WIDTH,0],[WIDTH-PAD_WIDTH,PAD_HEIGHT],[WIDTH,PAD_HEIGHT]]
paddle1_vel=[0,0]
paddle2_vel=[0,0]
score1=0
score2=0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos[0] = WIDTH/2 
    ball_pos[1] = HEIGHT/2
    
    if direction==LEFT:
        ball_vel=[-1,-0.5]
    elif direction==RIGHT:
        ball_vel=[1,-0.5]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    balldir=int(2*random.random())
    if balldir==1:
        spawn_ball(RIGHT)
    elif balldir==0:
        spawn_ball(LEFT)
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]   
    
    # update paddle
    if paddle1_pos[0][1]<= HEIGHT-PAD_HEIGHT and paddle1_pos[0][1]>=0:
        paddle1_pos[0][1] += paddle1_vel[1]
        paddle1_pos[1][1] += paddle1_vel[1]
        paddle1_pos[2][1] += paddle1_vel[1]    
        paddle1_pos[3][1] += paddle1_vel[1]
        
        if paddle1_pos[0][1] == HEIGHT-PAD_HEIGHT:
            paddle1_pos[0][1] -= 4
            paddle1_pos[1][1] -= 4
            paddle1_pos[2][1] -= 4  
            paddle1_pos[3][1] -= 4
        elif paddle1_pos[0][1]==0:
            paddle1_pos[0][1] += 4
            paddle1_pos[1][1] += 4
            paddle1_pos[2][1] += 4  
            paddle1_pos[3][1] += 4
        
    if paddle2_pos[0][1]<= HEIGHT-PAD_HEIGHT and paddle2_pos[0][1]>=0:
        paddle2_pos[0][1] += paddle2_vel[1]    
        paddle2_pos[1][1] += paddle2_vel[1]
        paddle2_pos[2][1] += paddle2_vel[1]   
        paddle2_pos[3][1] += paddle2_vel[1]  
       
        if paddle2_pos[0][1] >= HEIGHT-PAD_HEIGHT:
            paddle2_pos[0][1] -= 4
            paddle2_pos[1][1] -= 4
            paddle2_pos[2][1] -= 4  
            paddle2_pos[3][1] -= 4
        elif paddle2_pos[0][1]<=0:
            paddle2_pos[0][1] += 4
            paddle2_pos[1][1] += 4
            paddle2_pos[2][1] += 4  
            paddle2_pos[3][1] += 4
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS,1,"White", "White")
    # update paddle's vertical position, keep paddle on the screen
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, 'White',"White")
    canvas.draw_polygon(paddle2_pos, 1, 'White',"White")
    # determine whether paddle and ball collide
       
    # if the ball reaches the left edge of the canvas 
    if ball_pos[0]-BALL_RADIUS<=PAD_WIDTH:
            # if the ball collides with the pad
        if ball_pos[1]>=paddle1_pos[1][1] and ball_pos[1]<=paddle1_pos[2][1]:
            ball_vel[0]*=-1.1
        else:
            score2+=1
            spawn_ball(RIGHT)
    # if the ball reaches the right edge of the canvas 
    if ball_pos[0]+BALL_RADIUS>=WIDTH-PAD_WIDTH:
            # if the ball collides with the pad
        if ball_pos[1]>=paddle2_pos[1][1] and ball_pos[1]<=paddle2_pos[2][1]:
            ball_vel[0]*=-1.1
        else:
            score1+=1
            spawn_ball(LEFT)
    elif ball_pos[1]-BALL_RADIUS<=0:
        ball_vel[1]*=-1
    elif ball_pos[1]+BALL_RADIUS>=HEIGHT:    
        ball_vel[1]*=-1
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 3,HEIGHT/3], 32, "White")
    canvas.draw_text(str(score2), [WIDTH*2 / 3-16,HEIGHT/3], 32, "White")
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if(key==simplegui.KEY_MAP['s']):
        paddle1_vel[1]=4
    if(key==simplegui.KEY_MAP['down']):
        paddle2_vel[1]=4
    if(key==simplegui.KEY_MAP['w']):
        paddle1_vel[1]=-4
    if(key==simplegui.KEY_MAP['up']):
        paddle2_vel[1]=-4
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if(key==simplegui.KEY_MAP['s']):
        paddle1_vel[1]=0
    if(key==simplegui.KEY_MAP['down']):
        paddle2_vel[1]=0
    if(key==simplegui.KEY_MAP['w']):
        paddle1_vel[1]=0
    if(key==simplegui.KEY_MAP['up']):
        paddle2_vel[1]=0    
    
def restart_button_handler():
    global score1, score2
    score1=0
    score2=0
    new_game()
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", restart_button_handler)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
