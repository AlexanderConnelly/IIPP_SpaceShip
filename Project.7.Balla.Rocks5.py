# program template for Spaceship
import simplegui
import math
import random

## USES MP3's!!! Run in Chrome or Safari, not Firefox, sorry

# globals for user interface
WIDTH = 1200
HEIGHT = 900
score = 0
lives = 0
time = 0
g_play=False
pew = 0

BOOST = .3
FRICTION=.03
ROTATION_VEL=.075

missile_vel=(0,0)
thrust_play=0
astroids_list = set()
missile_list = set()

reset_animation = True
time_index = -60
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
nebula_info = ImageInfo([1280/2, 1024/2], [1280, 1024])
nebula_image = simplegui.load_image("http://cdn.spacetelescope.org/archives/images/wallpaper2/heic0506a.jpg")


# splash image
splash_info = ImageInfo([1675/2, 477/2], [1675, 477])
splash_image = simplegui.load_image("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/SpashScreen.png")

# ship image
ship_info = ImageInfo([75, 250/2], [150, 250], 35)
ship_image = simplegui.load_image("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/alien%20spaceship.png")
# ship image with thrusters animation:
ship_image1 = simplegui.load_image("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/alien%20spaceship%20thrusters1.png")
ship_image2 = simplegui.load_image("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/alien%20spaceship%20thrusters2.png")
ship_image3 = simplegui.load_image("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/alien%20spaceship%20thrusters3.png")
ship_image4 = simplegui.load_image("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/alien%20spaceship%20thrusters4.png")
ship_image5 = simplegui.load_image("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/alien%20spaceship%20thrusters5.png")
ship_image6 = simplegui.load_image("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/alien%20spaceship%20thrusters6.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([45,45], [90,90], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack1 = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/Old%20School.mp3")
soundtrack1.set_volume(.5)
soundtrack2 = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/Still.mp3")

missile_sound = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/PEW_Fast.mp3")
missile_sound1 = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/PEW_Fast.mp3")
missile_sound2 = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/PEW_Fast.mp3")
missile_sound3 = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/PEW_Fast.mp3")
missile_sound4 = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/PEW_Fast.mp3")
missile_sound5 = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/PEW_Fast.mp3")

missile_sound.set_volume(.5)
missile_sound1.set_volume(.5)
missile_sound2.set_volume(.5)
missile_sound3.set_volume(.5)
missile_sound4.set_volume(.5)
missile_sound5.set_volume(.5)

ship_thrust_sound = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/Boosters.mp3")
ship_thrust_sound.set_volume(.1)
explosion_sound = simplegui.load_sound("http://googledrive.com/host/0B0Jk8Tq7HujnazNLdmFVTnZETkE/Fadoo%20Boom.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = []
    def draw(self,canvas):
        #keep ship on canvas:
        if self.pos[0] < 0:
            self.pos[0] = WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1]= 0
        
        #draw flamming trail
        if self.thrust:
            thrust_frame= random.randrange(1,7)
            if thrust_frame == 1:
                canvas.draw_image(ship_image1,ship_info.get_center(),ship_info.get_size(),self.pos,  (75,100),self.angle-math.radians(90))
            elif thrust_frame == 2:
                canvas.draw_image(ship_image2,ship_info.get_center(),ship_info.get_size(),self.pos,  (75,100),self.angle-math.radians(90)) 
            elif thrust_frame == 3:
                canvas.draw_image(ship_image3,ship_info.get_center(),ship_info.get_size(),self.pos,  (75,100),self.angle-math.radians(90))
            elif thrust_frame == 4:
                canvas.draw_image(ship_image4,ship_info.get_center(),ship_info.get_size(),self.pos,  (75,100),self.angle-math.radians(90))
            elif thrust_frame == 5:
                canvas.draw_image(ship_image5,ship_info.get_center(),ship_info.get_size(),self.pos,  (75,100),self.angle-math.radians(90))
            elif thrust_frame == 6:
                canvas.draw_image(ship_image2,ship_info.get_center(),ship_info.get_size(),self.pos,  (75,100),self.angle-math.radians(90))
            
        else:
            canvas.draw_image(ship_image,self.image_center,ship_info.get_size(),self.pos,  (75,100),self.angle-math.radians(90))
        
        
    def update(self):
        #update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        #calculate vector amounts in X and Y disp
        
        forward = [math.cos(self.angle),math.sin(self.angle)]
        if self.thrust:
            self.vel[0] += forward[0]*BOOST
            self.vel[1] += forward[1]*BOOST
        missile_vel = angle_to_vector(self.angle) * 45
        
        #update friction
        self.vel[0] *= (1-FRICTION)
        self.vel[1] *= (1-FRICTION)
        
        #update facing direction
        self.angle += self.angle_vel
        global thrust_play
        thrust_play+=1
    def thrusters(self):
        if self.thrust == True:
            self.thrust = False
        else:
            self.thrust = True
        
        return self.thrust
    
    def steer(self,direction):
        if direction =='left':
            self.angle_vel = -ROTATION_VEL
        if direction == 'right': 
            self.angle_vel = ROTATION_VEL
        if direction == 'none':
            self.angle_vel = 0
    
    def get_pos(self):
        missile_vel = angle_to_vector(self.angle) * 45
        fire_location =(self.pos[0]+missile_vel[0]*25,self.pos[1]+missile_vel[1]*25)
        return fire_location
    
    def get_velocity(self):
        return self.vel
    def get_angle(self):
        return self.angle
    def collide(self,other_sprite):
        #self.pos,self.radius
        o_pos = other_sprite.get_position()
        o_rad = other_sprite.get_radius()
        
        if math.sqrt((self.pos[0]-o_pos[0])**2+(self.pos[1]-o_pos[1])**2) > (o_rad+self.radius):
            return False
        else:
            return True
            
            
    def group_collide(self,group):
        n_collisions = 0
        global lives
        for sprite in list(group):
            if self.collide(sprite) == True:
                # loose a life, reset sprite to center of screen, play boom sound
                lives -= 1
                group.remove(sprite)
                self.pos[0] = (WIDTH/2)
                self.pos[1] = (HEIGHT/2)
                #animate explosion
                    
                self.vel[0] = 0
                self.vel[1] = 0
                if reset_animation == False:
                    explosion_sound.play()
        return n_collisions
    
    
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
        self.forward = (0,0)
        self.fired = False
        self.is_missile = False
    def draw(self, canvas):
        #keep ship on canvas:
        if self.pos[0] < 0:
            self.pos[0] = WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1]= 0
        canvas.draw_image(self.image, self.image_center,self.image_size,self.pos, self.image_size,self.angle)
        #spin if available
        self.angle+=self.angle_vel
    def update(self):
        #update position:
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.age += 1
        
        if self.fired:
            missile_vel = angle_to_vector(self.angle) 
            self.vel[0] += missile_vel[0] * 15
            self.vel[1] += missile_vel[1] * 15
            self.fired = False
        if self.age >= self.lifespan and self.is_missile == True:
            missile_list.remove(self)
    def fire(self,velocity,angle):
        
        self.fired = True
        self.is_missile = True
        self.vel[0] = velocity[0]
        self.vel[1] = velocity[1]
        self.angle = angle
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self,other_sprite):
        #self.pos,self.radius
        o_pos = other_sprite.get_position()
        o_rad = other_sprite.get_radius()
        
        if math.sqrt((self.pos[0]-o_pos[0])**2+(self.pos[1]-o_pos[1])**2) > (o_rad+self.radius):
            return False
        else:
            return True
    def group_collide(self,group):
        
        for sprite in list(group):
            if self.collide(sprite):
                group.remove(sprite)
                return True
        
        return False
    def group_group_collide(self,group_a,group_b):
        n_collisions = 0
        remove_list = []
        for sprite in list(group_a):
            if sprite.group_collide(group_b):
                n_collisions += 1
                remove_list.append(sprite)
        
        return set(remove_list)
            
def draw(canvas):
    global time,lives,reset_animation, time_index, astroids_list,missile_list,score
    
    # animate background
    time +=1
    wtime = (time) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    
    #animate nebula
    ZOOM = .1
    nebula_center = [WIDTH / 2, HEIGHT / 2]
    ship_center = my_ship.get_pos()
    
    if ship_center[0] <= WIDTH / 2 and ship_center[1] <= HEIGHT / 2:
        nebula_center[0] += ((WIDTH*ZOOM)/2) * ((WIDTH/2-ship_center[0]) / (WIDTH / 2)) 
        nebula_center[1] += (HEIGHT*ZOOM)/2 * ((HEIGHT/2 - ship_center[1]) / (HEIGHT / 2)) 
    elif ship_center[0] > WIDTH / 2 and ship_center[1] <= HEIGHT / 2:
        nebula_center[0] -= ((WIDTH*ZOOM)/2) * ((ship_center[0]-WIDTH/2) / (WIDTH / 2)) 
        nebula_center[1] += (HEIGHT*ZOOM)/2 * ((HEIGHT/2 - ship_center[1]) / (HEIGHT / 2))
    elif ship_center[0] > WIDTH / 2 and ship_center[1] > HEIGHT / 2:
        nebula_center[0] -= ((WIDTH*ZOOM)/2) * ((ship_center[0] - WIDTH/2) / (WIDTH / 2)) 
        nebula_center[1] -= (HEIGHT*ZOOM)/2 * ((ship_center[1] - HEIGHT/2) / (HEIGHT / 2))
    elif ship_center[0] <= WIDTH / 2 and ship_center[1] > HEIGHT / 2:
        nebula_center[0] += ((WIDTH*ZOOM)/2) * ((WIDTH/2-ship_center[0]) / (WIDTH / 2)) 
        nebula_center[1] -= (HEIGHT*ZOOM)/2 * ((ship_center[1] - HEIGHT/2) / (HEIGHT / 2))
        
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), nebula_center, [WIDTH+WIDTH*ZOOM, HEIGHT+HEIGHT*ZOOM])
    
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    time_disp="Time = "+str(time//60)
    
    #text HUD display
    canvas.draw_text(time_disp,(WIDTH/2,25),25,"White")
    canvas.draw_text(str("Lives: "+str(lives)),(25,25),25,"White")
    canvas.draw_text(str("Score: "+ str(score)),(WIDTH-150,25),25,"White")
    canvas.draw_text("Credit ESA/Hubble                      Press 'g' to toggle random Gangster Soundtrack!!! (Explicit)",(25,HEIGHT-25),25,"White")                
    
    # if dead, explode and reset game, display text exlpaining stuff, then redraw ship and reset scores and such:
    if lives <= 0 and reset_animation == False:
        reset_animation = True
        time = 0
    elif lives <= 0 and reset_animation == True :
        astroids_list = set()
        missile_list = set()
        canvas.draw_image(splash_image, splash_info.get_center(),splash_info.get_size(),(WIDTH/2,HEIGHT/2),(WIDTH,HEIGHT*2/3)) 
        
    else:
        my_ship.draw(canvas)
    # draw ship and sprites
    
    for rock in astroids_list:
        rock.draw(canvas)
        rock.update()
    # check for collisions
    for missile in missile_list:
        missile.draw(canvas)
        missile.update()
        
    remove_list = a_missile.group_group_collide(missile_list,astroids_list)
    for r in remove_list:
        missile_list.discard(r)
        remove_list.discard(r)
        score += 1
    my_ship.update()
    
    
    #ship with asteroids
    my_ship.group_collide(astroids_list)
    #asteroids with missiles
    
    
    missile_list        
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    if reset_animation == False and score < 10:
        a_rock = Sprite([random.randrange(0,WIDTH), random.randrange(0,HEIGHT)], [random.choice([-1,1])*random.random(),random.choice([-1,1])*random.random()], random.choice([-1,1])*random.random(), random.choice([-1,1])*random.random()*.1, random.choice([asteroid_image,asteroid_image1,asteroid_image2]), asteroid_info)
        astroids_list.add(a_rock)
    elif reset_animation == False and score >=10:
        for i in range(0,score//10):
            a_rock = Sprite([random.randrange(0,WIDTH), random.randrange(0,HEIGHT)], [random.choice([-1,1])*random.random(),random.choice([-1,1])*random.random()], random.choice([-1,1])*random.random(), random.choice([-1,1])*random.random()*.1, random.choice([asteroid_image,asteroid_image1,asteroid_image2]), asteroid_info)
            astroids_list.add(a_rock)    
        
    #for rock in range(0,1):
        #a_rock = Sprite([random.randrange(0,WIDTH), random.randrange(0,HEIGHT)], [random.choice([-1,1])*random.random(),random.choice([-1,1])*random.random()], random.choice([-1,1])*random.random(), random.choice([-1,1])*random.random()*.1, random.choice([asteroid_image,asteroid_image1,asteroid_image2]), asteroid_info)
        #astroids_list.append(a_rock)
        
    
def keydown(key):
    global g_play,pew, a_missile
    #SOUND TESTS
    if key==simplegui.KEY_MAP["w"] or key==simplegui.KEY_MAP["up"]:
        ship_thrust_sound.play()
        
        my_ship.thrusters()
        
    #gangster old school tribute     
    elif key==simplegui.KEY_MAP["g"]:
        if g_play==False:
            g_play=True
            #soundtrack1.play()
            if random.choice([1,2])==1:
                soundtrack1.play()
            else:
                soundtrack2.play()
        elif g_play==True:
            soundtrack1.pause()
            soundtrack2.pause()
            g_play=False
    
    elif key==simplegui.KEY_MAP["a"] or key==simplegui.KEY_MAP["left"]:
        my_ship.steer("left")
    elif key==simplegui.KEY_MAP["d"] or key==simplegui.KEY_MAP["right"]:
        
        my_ship.steer("right")    
    elif key==simplegui.KEY_MAP["space"]:
        
        a_missile = Sprite(my_ship.get_pos(), missile_vel, 0, 0, missile_image, missile_info, missile_sound1)
        a_missile.fire(my_ship.get_velocity(),my_ship.get_angle())
        missile_list.add(a_missile)
        if pew == 0 and reset_animation == False:
            missile_sound1.play()
            pew += 1
        elif pew == 1 and reset_animation == False:
            missile_sound2.play()
            pew += 1
        elif pew == 2 and reset_animation == False:
            missile_sound3.play()
            pew += 1
        elif pew == 3 and reset_animation == False:
            missile_sound4.play()
            pew += 1
        elif pew == 4 and reset_animation == False:
            missile_sound5.play()
            pew += 1
        elif pew == 5 and reset_animation == False:
            missile_sound.play()    
            pew = 0
    
        
def keyup(key):
    
    if key==simplegui.KEY_MAP["w"] or key==simplegui.KEY_MAP["up"]:
        ship_thrust_sound.pause()
        ship_thrust_sound.rewind()
        my_ship.thrusters()    
        
    elif key==simplegui.KEY_MAP["a"] or key==simplegui.KEY_MAP["left"]:
        my_ship.steer("none")
    elif key==simplegui.KEY_MAP["d"] or key==simplegui.KEY_MAP["right"]:
        my_ship.steer("none")  
def mouse_handler(pos):
    global lives, reset_animation, time,score
    if reset_animation == True:
        reset_animation = False
        lives = 3
        time = 0
        score = 0
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0],math.radians(90), ship_image, ship_info)
a_rock = Sprite([random.randrange(0,WIDTH), random.randrange(0,HEIGHT)], [random.choice([-1,1])*random.random(),random.choice([-1,1])*random.random()], random.choice([-1,1])*random.random(), random.choice([-1,1])*random.random()*.1, random.choice([asteroid_image,asteroid_image1,asteroid_image2]), asteroid_info)
a_missile = Sprite([0, 0], [-1,1], 0, 0, missile_image, missile_info)
   
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_handler)
timer = simplegui.create_timer(1000, rock_spawner)

# get things rolling
timer.start()
frame.start()
