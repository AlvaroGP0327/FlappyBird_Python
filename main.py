import pygame, sys, os
from random import randint, choice

pygame.init()
size = (576,1024) 
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#sky background
class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/background-day.png').convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(topleft=(0,0))
        
#Ground in movement
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/base.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(0,890))
    
    def initial_position(self):
        self.rect.x = 576
    
    def ground_movement(self):
        self.rect.left -= 1    
        if self.rect.right == 0:
            self.rect.left = 576
            
    def update(self):
        self.ground_movement()

class Pipe(pygame.sprite.Sprite):
    def __init__(self,position, is_flipped=False):
        super().__init__()
        self.image = pygame.image.load('assets/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        
        
        if is_flipped:
            self.flip_pipe()
            self.rect = self.image.get_rect(bottomleft=(600,position))
        else:
            self.rect = self.image.get_rect(topleft=(600,position))
 
    
    def flip_pipe(self):
        self.image = pygame.transform.rotate(self.image,180)   

    def movement_pipe(self):
        self.rect.x -= 5
    
    def destroy_pipes(self):
        if self.rect.right < 0:
            self.kill()
    
    def update(self):
        self.movement_pipe()
        self.destroy_pipes()

#Instances
sky = Sky()
ground = Ground()
ground_2 = Ground()
ground_2.initial_position()

#Sprite Groups
sky_group = pygame.sprite.GroupSingle()
sky_group.add(sky)

ground_group = pygame.sprite.Group()
ground_group.add(ground)
ground_group.add(ground_2)

obstacle_group = pygame.sprite.Group()

#Timer for create random pipes obstalces.
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,2800)

pipe_gap = -300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == obstacle_timer:
            #set position before instantiate pipes
            #random position for bottom pipe
            topleft_pipe_position = choice([400,500,600,750]) #topleft
            pipe = Pipe(topleft_pipe_position)
            #get the y position relative to bottom pipe position
            top_pipe_position = pipe.rect.topleft[1]
            top_pipe_position += pipe_gap
            pipe_2 = Pipe(top_pipe_position,is_flipped=True)
            obstacle_group.add(pipe)
            obstacle_group.add(pipe_2)
            
    ground_group.update()
    obstacle_group.update()
    sky_group.draw(screen)
    obstacle_group.draw(screen)
    ground_group.draw(screen)
    
    pygame.display.update()
    
    clock.tick(60)    