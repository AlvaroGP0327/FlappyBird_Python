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
        self.image = pygame.image.load('assets/background-day.png').convert()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(topleft=(0,0))
        
#Instances
sky = Sky()

#Sprite Groups
sky_group = pygame.sprite.GroupSingle()
sky_group.add(sky)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    sky_group.draw(screen)
    pygame.display.update()
    
    clock.tick(60)    