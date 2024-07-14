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
    def __init__(self, is_flipped=False):
        super().__init__()
        self.image = pygame.image.load('assets/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        
        if is_flipped:
            self.flip_pipe()
        self.rect = self.image.get_rect(bottom=1300 if not is_flipped else 310)
        
        self.initial_position()
     
    def flip_pipe(self):
        self.image = pygame.transform.rotate(self.image,180)
        
    
    def initial_position(self):
        self.rect.right = 524        

    def animation_pipe(self):
        pass
    
    def update(self):
        self.initial_position()

#Instances
sky = Sky()
ground = Ground()
ground_2 = Ground()
ground_2.initial_position()
pipe = Pipe()
pipe_2 = Pipe(is_flipped=True)


#Sprite Groups
sky_group = pygame.sprite.GroupSingle()
sky_group.add(sky)

ground_group = pygame.sprite.Group()
ground_group.add(ground)
ground_group.add(ground_2)

obstacle_group = pygame.sprite.Group()
obstacle_group.add(pipe)
obstacle_group.add(pipe_2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    sky_group.draw(screen)
    ground_group.update()
    obstacle_group.draw(screen)
    ground_group.draw(screen)
    obstacle_group.update()
    
    
    pygame.display.update()
    
    clock.tick(60)    