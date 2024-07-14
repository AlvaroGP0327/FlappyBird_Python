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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    sky_group.draw(screen)
    ground_group.draw(screen)
    ground_group.update()
 
    pygame.display.update()
    
    clock.tick(60)    