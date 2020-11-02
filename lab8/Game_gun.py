import math
import pygame
from pygame.draw import *
from pygame.event import *
from random import *
import time

# start condition
score = 0
height_screen = 700
width_screen = 1200
FPS = 30
dt = 0.5
# gun
gun_width = 25
gun_length = 100
x_start_gun = 25
y_start_gun = height_screen - 10
direction_start = math.pi / 3
# balls
count_ball = 1
min_speed_ball = 20
max_speed_ball = 60
radius_ball = gun_width / 2
balls = []
acceleration = 1
# target
x_left_target = width_screen // 2
x_right_target = width_screen
y_top_target = 0
y_bottom_target = height_screen
min_speed_target = 10
max_speed_target = 30
min_radius_target = 5
max_radius_target = 20
count_target = 4
targets = []


screen = pygame.display.set_mode((width_screen, height_screen))

colors = [(0,0,0), # black
          (173, 253, 47), # green_yellow
          (0, 128, 0) # green
         ]

class Ball():
    def __init__(self, radius, x, y, angle, screen):
        
        self.screen = screen
        self.x = x 
        self.y = y
        self.r = radius
        self.speed = randint(min_speed_ball, max_speed_ball)
        self.angle = angle
        self.a = acceleration
        self.vx = self.speed * math.cos(self.angle)
        self.vy = -self.speed * math.sin(self.angle)
        self.color = colors[randint(1,1)]
        
    def move(self):
        if self.x >= width_screen - self.r or self.r >= self.x:
            self.vx *= -0.5
            if self.x <= self.r:
                self.x = self.r
            else:
                self.x = width_screen - self.r
        if self.y >= height_screen - self.r:
            self.vy *= -0.5
            self.vx *= 0.95
            self.y = height_screen - self.r
        self.x += self.vx
        self.vy += self.a * dt
        self.y += self.vy * dt
        circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.r))
        return self.x, self.y, self.r
    
    def delete(self):
        
        print("!")

class Gun():
    def __init__(self, x, y):
        
        self.screen = screen
        self.x = x
        self.y = y
        self.width = gun_width
        self.length = gun_length
        self.height = height_screen
        self.direction = direction_start
        self.color = colors[1]
        
    def turn(self, x, y):
        if x != 0:
            self.direction = math.atan((self.height - y) / x)
        return self.direction
        
    def draw(self):
        
        x = int(self.x)
        y = int(self.y)
        w = self.width
        l = self.length
        d = self.direction
        
        polygon(self.screen, self.color,
                ((x, y),
                 (x - int(w * math.sin(d)), y - int(w * math.cos(d))),
                 (x - int(w * math.sin(d) - l * math.cos(d)), y - int(w * math.cos(d) + l * math.sin(d))),
                 (x + int(l * math.cos(d)), y - int(l * math.sin(d)))
                ))
        return x - w * math.sin(d) // 2 + l * math.cos(d), y - l * math.sin(d) - w * math.cos(d) // 2


class Target():
    def __init__(self):
        
        self.screen = screen
        self.x = randint(x_left_target, x_right_target)
        self.y = randint(y_top_target, y_bottom_target)
        self.r = randint(min_radius_target, max_radius_target)
        self.angle = random() * 2 * math.pi
        self.color = colors[randint(2,2)]
        self.speed = randint(min_speed_target, max_speed_target)
    
    def draw(self):
        
        circle(self.screen, self.color, (self.x, self.y), self.r)
        
    def move(self):
        
        if self.x >= width_screen - self.r:
            self.angle = math.pi / 2 + random() * math.pi
        if self.y >= height_screen - self.r:
            self.angle = random() * math.pi
        if self.r >= self.x:
            self.angle = random() * math.pi - math.pi / 2
        if self.r >= self.y:
            self.angle = random() * math.pi + math.pi
        self.x += int(self.speed * math.cos(self.angle))
        self.y -= int(self.speed * math.sin(self.angle))
        target.draw()
    
    
    def hit(self, x_ball, y_ball, r_ball):

        distance = math.sqrt((x_ball - self.x) ** 2 + (y_ball - self.y) ** 2)
        if distance <= self.r + r_ball:
            target.delete()
            ball.delete()
#             score = score + 1

    def delete(self):
        
        print("!!!")


clock = pygame.time.Clock()
finished = False

# generetion parameters of the gun
gun = Gun(x_start_gun, y_start_gun)

# generetion parameters of the first target
for target in range(count_target):
    targets.append(Target())

while not finished:
    clock.tick(FPS)
    pygame.display.update()
    screen.fill(colors[0])
    x_start_ball, y_start_ball = gun.draw()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            angle = gun.turn(x_mouse, y_mouse)
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                balls.append(Ball(radius_ball, x_start_ball, y_start_ball, angle, screen))
    for ball in balls:
        x_ball, y_ball, r_ball = ball.move()    
        target.hit(x_ball, y_ball, r_ball)    
    for target in targets:
        target.move()
        
pygame.quit()