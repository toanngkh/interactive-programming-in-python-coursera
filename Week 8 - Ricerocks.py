# Ricerocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
canvas_center = [WIDTH / 2, HEIGHT / 2]
key_status = 'up'
rock_group = set([])
missile_group = set([])
explosion_group = set([])
remove_sprite = False
ship_collision = False
mis_collision = False
started = False
bonus_time = 0
bonus_spawned = False
message = 'Welcome to RiceRocks retro! This game is customized in that rocks spawn increase when your score get higher and bonus life appears once per game as your only second change when you have 1 life left.'

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([10,8], [20, 16], 5, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# heart image
heart_info = ImageInfo([25, 25], [50, 50], 25)
heart_image = simplegui.load_image("https://dl.dropbox.com/s/yjfiipqe6w5nc7q/heart_50x50.png")

# hearts image
hearts_info = ImageInfo([25, 25], [50, 50], 25)
hearts_image = simplegui.load_image("https://dl.dropbox.com/s/hpp8v9cqgwxehv0/hearts_1200x50.png")

# lives image
lives_info = ImageInfo([62, 16], [124, 32])
lives_image = simplegui.load_image("https://dl.dropbox.com/s/nhhz57w0q07wfnq/Lives_yellow_124x32.png")

# scores image
scores_info = ImageInfo([70, 15], [140, 30])
scores_image = simplegui.load_image("https://dl.dropbox.com/s/sa8zz2xgp3ffyp4/Scores_140x30.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(sprite_set, canvas):
    # update and draw sprite_set
    remove = set([])
    for sprite in sprite_set:
        if sprite.update():
            remove.add(sprite)
        sprite.update()
        sprite.draw(canvas)
    sprite_set.difference_update(remove)
    
def group_collide(group, other_object):
    # detect collision between a member of the group (set) and other_object (sprite)
    # if there is collision, remove that member
    global ship_collision, mis_collision, explosion_group
    remove = set([])
    for member in group:
        if member.collide(other_object):
            if other_object == my_ship:
                ship_collision = True
            elif other_object == a_missile:
                mis_collision = True
            remove.add(member)
            # create explosion sprite at collision place to replace member and add to explosion group
            an_explosion = Sprite(member.pos, (0, 0), 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
    group.difference_update(remove)
    return True if ship_collision or mis_collision else False     
    
def group_group_collide(group1, group2):
    # detect collision between a member of a group w a member of the other group
    # update accordingly
    remove = set([])
    for member in group1:
        group_collide(group2, member)
        if mis_collision:
            remove.add(member)
    group1.difference_update(remove)
    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0.00
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(ship_image, self.image_center, self.image_size, 
                                self.pos, self.image_size, self.angle)
    def action(self, key, key_status):
        if key_status == 'down':
            if key == 37: # left
                self.angle_vel -= 0.08
            elif key == 39: # right
                self.angle_vel += 0.08
            elif key == 38: # up
                self.thrust = True
                self.image_center = [135, 45]
                ship_thrust_sound.play()
            elif key == 32: # space
                global a_missile, missile_group
                # parameters
                orient = angle_to_vector(self.angle)
                m_vel = [self.vel[0] + 10 * orient[0], self.vel[1] + 10 * orient[1]]
                m_pos = [self.pos[0] + (self.image_size[0] / 2) * orient[0], 
                         self.pos[1] + (self.image_size[0] / 2) * orient[1]]
                # create object
                a_missile = Sprite(m_pos, m_vel, self.angle, 0, missile_image, missile_info, missile_sound)
                missile_group.add(a_missile)
        else:
            if key == 37 or key == 39:
                my_ship.angle_vel = 0
            elif key == 38:
                self.thrust = False
                self.image_center = [45, 45]
                ship_thrust_sound.rewind()
                
    def update(self):
        global score, level
        # turn ship 
        self.angle += self.angle_vel
        if self.thrust:
            # give ship's vel direction
            acceleration = angle_to_vector(self.angle)
            vel_x = 4 * acceleration[0]
            vel_y = 4 * acceleration[1]
            self.vel = [vel_x, vel_y]
        else:
            # friction slows ship down when not thrusting:
            self.vel[0] *= 0.99
            self.vel[1] *= 0.99
        # update ship's position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
                    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]], self.image_size, 
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0], self.image_center[1]], self.image_size, 
                              self.pos, self.image_size, self.angle)
            
    def update(self):
        global remove_sprite
        # update orientation and position
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]        
        self.pos[1] += self.vel[1]

        # wrap around screen
        if self.pos[0] < 0:
            self.pos[0] += WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[1] < 0:
            self.pos[1] += HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0
        # update age
        self.age += 1
        if self.age > self.lifespan:
            return True 
        else:
            return False 
        
    def collide(self, other_object):
        return True if dist(self.pos, other_object.pos) <= self.radius + other_object.radius else False
            
def draw(canvas):
    global time, started, lives, score, ship_collision, mis_collision, rock_group, missile_group, level, my_ship
    global bonus_time, bonus_spawned
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # user interface
#    canvas.draw_text('Score: ', [WIDTH / 10, HEIGHT / 8], 24, 'white', 'monospace')
#    canvas.draw_text('Lives: ', [WIDTH / 8 * 5.5, HEIGHT / 8], 24, 'white', 'monospace')
#    canvas.draw_text(str(lives), [WIDTH / 8 * 7, HEIGHT / 8], 24, 'white')
    canvas.draw_text(str(score), [WIDTH / 10 * 2.5, HEIGHT / 8 - 15], 24, 'white', 'monospace')
    canvas.draw_image(scores_image, scores_info.get_center(), scores_info.get_size(), [WIDTH / 7, HEIGHT / 8 - 20], scores_info.get_size())
    canvas.draw_image(lives_image, lives_info.get_center(), lives_info.get_size(), [WIDTH / 8 * 5.6, HEIGHT / 8 - 20], lives_info.get_size())
    for life in range(lives):
        canvas.draw_image(heart_image, heart_info.get_center(), heart_info.get_size(), [WIDTH / 8 * 6.5 + 50*life, HEIGHT / 8 - 25], heart_info.get_size())
    
    # bonus life
#    current_heart_index = (time % 24) // 1
#    heart_center = hearts_info.get_center()
#    heart_size = hearts_info.get_size()
#    current_heart_center = [heart_center[0] + current_heart_index * heart_size[0], heart_center[1]]
#    canvas.draw_image(hearts_image, current_heart_center, heart_size, [WIDTH / 2, HEIGHT / 2], heart_size)
#    time += 0.1
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    if started:
        my_ship.update()
        soundtrack.play()
        
    # update and draw sprite groups
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    
    # detect collision between rock_group (set) and ship 
    group_collide(rock_group, my_ship)

    # deduct live if ship collides with rock
    if ship_collision:
        lives -= 1
        ship_collision = False
    
    # if lives = 1, bonus lives appears once per game
    current_heart_index = (time % 24) // 1
    heart_center = hearts_info.get_center()
    heart_size = hearts_info.get_size()
    current_heart_center = [heart_center[0] + current_heart_index * heart_size[0], heart_center[1]]
    if lives == 1 and not bonus_spawned:
        canvas.draw_image(hearts_image, current_heart_center, heart_size, bonus_life.pos, heart_size)
        time += 0.01
        if bonus_life.collide(my_ship):
            lives += 1
            bonus_spawned = True 
    
    # game stops if lives reach 0
    if lives == 0:    
        started = False
        
    # detect collision of missile gropu and rock group
    group_group_collide(missile_group, rock_group)
    
    # increase score if missile hit rock:
    if mis_collision:
        score += 10
        mis_collision = False

    # draw splash screen and reset game if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        score = 0
        lives = 3
        level = 1
        rock_group = set([])
        missile_group = set([])
        remove_sprite = False
        ship_collision = False
        mis_collision = False
        soundtrack.rewind()
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], math.pi, ship_image, ship_info)
        
# keydown handler
def keydown(key):
    if started:
        key_status = 'down'
        my_ship.action(key, key_status)
    
# keyup handler
def keyup(key):
    key_status = 'up'
    my_ship.action(key, key_status)
    
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
     
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, rock_group
    # parameters
    rock_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    # prevent a_rock from spawning right at ship's position causes death
    if dist(rock_pos, my_ship.pos) <= a_rock.radius + my_ship.radius:
        rock_pos[0] += my_ship.radius * 2
        rock_pos[1] += my_ship.radius * 2
    rock_vel = [random.randrange(-1, 1), random.randrange(-1, 1)]
    lower = -0.1
    upper = 0.1
    range_width = upper - lower
    rock_angvel = random.random() * range_width + lower
    rock_angle = random.random()
    # create object
    a_rock = Sprite(rock_pos, rock_vel, rock_angle, rock_angvel, asteroid_image, asteroid_info)
    if started:
        # numbers of rocks increase when your scores get higher:
        if score <= 50:
            while len(rock_group) <= 2:
                rock_group.add(a_rock)
                break
        elif 50 < score <= 100:
            while len(rock_group) <= 4:
                rock_group.add(a_rock)
                break
        elif 100 < score <= 150:
            while len(rock_group) <= 8:
                rock_group.add(a_rock)
                break
        elif 150 < score:
            while len(rock_group) <= 12:
                rock_group.add(a_rock)
                break
                
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], math.pi, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0.9, 0.9], 0, 0.01, asteroid_image, asteroid_info)
bonus_life = Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], [0, 0], 0, 0, hearts_image, hearts_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
label = frame.add_label(message)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
