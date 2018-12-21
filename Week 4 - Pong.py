# Implementation of classic arcade game Pong

import simplegui
import random
import math
# initialize globals - pos and vel encode vertical info for paddles
#---canvas
w = 600			# canvas width
h = 400			# canvas height       
r = 20			# ball radius
#---paddles
pw = 8			# pad width
ph = 80			# pad height
hpw = pw / 2	# half pad width = 4
hph = ph / 2	# half pad height = 40
p1_pos = h/2	# paddles verticle position = 200
p2_pos = h/2
p1_vel = 0		# paddles velocity
p2_vel = 0
#---ball
left = False
right = True
ball_pos = [w/2, h/2]
ball_vel = [0, 0]
#---players
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [w/2, h/2]
    if direction == left:
        ball_vel[0] = random.randrange(-200//60.0, -120/60.0)
        ball_vel[1] = random.randrange(-180/60.0, -60/60.0)
    if direction == right:
        ball_vel[0] = random.randrange(120/60.0, 200//60.0)
        ball_vel[1] = random.randrange(-180/60.0, -60/60.0)
    
# define event handlers
def new_game():
    # global p1_pos, p2_pos, p1_vel, p2_vel  # these are numbers
    global score1, score2  # these are ints
    dir = random.choice([left, right])
    spawn_ball(dir)
    score1 = 0
    score2 = 0
    
def draw(canvas):
    global score1, score2, p1_pos, p2_pos, p1_vel, p2_vel, ball_pos, ball_vel
            
    # draw mid line and gutters
    canvas.draw_line([w / 2, 0],[w / 2, h], 1, "White")
    canvas.draw_line([pw, 0],[pw, h], 1, "White")
    canvas.draw_line([w - pw, 0],[w - pw, h], 1, "White")
     
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # collision with floor and ceiling: ball bounces off
    if ball_pos[1] - r <= 0	or ball_pos[1] + r >= h - 1:
        ball_vel[1] = - ball_vel[1]		
    # collision with gutters: update score, spawn ball with opp direction
    if ball_pos[0] - r <= pw:		# collision with left gutter 
        if ball_pos[1] >= p1_pos - hph and ball_pos[1] <= p1_pos + hph:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] += 50/60.0		# ball speed is creased after  
            ball_vel[1] += 20/60.0		# boucning off the paddles
        else:
            score2 += 1
            spawn_ball(right)
        
    if ball_pos[0] + r >= w - pw - 1:	# collision with right gutter
        if ball_pos[1] >= p2_pos - hph and ball_pos[1] <= p2_pos + hph:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] -= 50/60.0
            ball_vel[1] -= 20/60.0
        else: 
            score1 += 1
            spawn_ball(left)
            
    
    # draw ball
    canvas.draw_circle(ball_pos, r, 1, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    if p1_pos + p1_vel >= hph and p1_pos + p1_vel <= h - hph:
        p1_pos += p1_vel
    if p2_pos + p2_vel >= hph and p2_pos + p2_vel <= h - hph:
        p2_pos += p2_vel
    
    # draw paddles
    canvas.draw_polygon(([0, p1_pos - hph], [pw, p1_pos - hph], [pw, p1_pos + hph], [0, p1_pos + hph]), 1, "red", "red")
    canvas.draw_polygon(([w - pw, p2_pos - hph], [w, p2_pos - hph], [w, p2_pos + hph], [w - pw, p2_pos + hph]), 1, "red", "red")
    # draw scores
    canvas.draw_text(str(score1), (235, 50), 24, "white") 
    canvas.draw_text(str(score2), (350, 50), 24, "white")
    
def keydown(key):
    global p1_vel, p2_vel
    if key == simplegui.KEY_MAP["w"]:
        p1_vel -= 4
    if key == simplegui.KEY_MAP["s"]:
        p1_vel += 4
    if key == simplegui.KEY_MAP["up"]:
        p2_vel -= 4
    if key == simplegui.KEY_MAP["down"]:
        p2_vel += 4
    
def keyup(key):
    global p1_vel, p2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        p1_vel = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        p2_vel = 0

def reset():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", w, h)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset, 100)

# start frame
new_game()
frame.start()
