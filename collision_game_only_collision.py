import os, sys, math, pygame, pygame.mixer
from pygame.locals import *
import random
import euclid

#Defining basic colors
black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0
blue = 0,0,255

colors = [black, red]

initial_velocity = 50;

#Define screen size
screen_size = screen_width, screen_height = 600, 400

class MyCircle:

    def __init__(self, position,size, color = (255, 255, 255), velocity = euclid.Vector2(0,0), width = 0):
        self.position = position
        self.size = size
        self.color = color
        self.width = width
        self.velocity = velocity

    def display(self):
        rx = int(self.position.x)
        ry = int(self.position.y)
        pygame.draw.circle(screen, self.color, (rx, ry), self.size, self.width)

    def move(self):
        self.position += self.velocity * dtime
        self.bounce()

    def change_velocity(self,velocity):
        self.velocity = velocity

    def bounce(self):
        if self.position.x <= self.size:
            self.position.x = 2*self.size - self.position.x
            self.velocity = self.velocity.reflect(euclid.Vector2(1,0))

        elif self.position.x >= screen_width - self.size:
            self.position.x = 2*(screen_width - self.size) - self.position.x
            self.velocity = self.velocity.reflect(euclid.Vector2(1,0))

        if self.position.y <= self.size:
            self.position.y = 2*self.size - self.position.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0,1))

        if self.position.y >= screen_height - self.size:
            self.position.y = 2*(screen_height - self.size) - self.position.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0,1))

    #Equation for distance between surfaces
    #d(t) = |A(t) - B(t)| - (Ra + Rb)
    def surface_distance(self, other, time):
        radiiAB = self.size + other.size
        posA = self.position + self.velocity * time# + 0.5*(self.accel * (time**2)) #do we need accel if gravity isn't at play?
        posB = other.position + other.velocity * time# + .5*(other.accel * (time ** 2))
        posAB = abs(posA - posB)
        return posAB - radiiAB

    def collide(self, other):
        if self.surface_distance(other, dtime) <= 0:
            collision_vector = self.position - other.position
            collision_vector.normalize()
            self.velocity = self.velocity.reflect(collision_vector)
            other.velocity = other.velocity.reflect(collision_vector)

def get_random_velocity():
    new_angle = random.uniform(0, math.pi**2)
    new_x = math.sin(new_angle)
    new_y = math.cos(new_angle)
    new_vector = euclid.Vector2(new_x, new_y)
    new_vector.normalize()
    new_vector *= initial_velocity
    return new_vector

#Setting the display and getting the Surface object
screen = pygame.display.set_mode(screen_size)

#Getting Clock object
clock = pygame.time.Clock()

#Setting a title to the window
#pygame.display.set_caption("First Class")
number_of_circles = 25
my_circles = []

for n in range(number_of_circles):
    size = random.randint(10,20)
    x = random.randint(size, screen_width - size)
    y = random.randint(size, screen_height-size)
    choice = random.randint(0,10)
    if choice == 1:
        color = red
    else:
        color = black
    velocity = get_random_velocity()
    my_circle = MyCircle(euclid.Vector2(x,y), size, color, velocity)
    my_circles.append(my_circle)

direction_tick = 0.0

#Defining variables for fps and continued running
fps_limit = 60
run_me = True
while run_me:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False

    #Limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime = dtime_ms/1000.0

    direction_tick += dtime
    if (direction_tick > 1.0):
        direction_tick = 0.0
        #random_circle = random.choice(my_circles)
        #new_velocity = get_random_velocity()
        #random_circle.change_velocity(new_velocity)

        #Clear the screen
    screen.lock()
    screen.fill(white)

    for i,my_circle in enumerate(my_circles):
        my_circle.move()
        for my_circle2 in my_circles[i+1:]:
            my_circle.collide(my_circle2)
        my_circle.display()

    screen.unlock()

    #Display everything in the screen
    pygame.display.flip()

#Quit game
pygame.quit()
sys.exit()
