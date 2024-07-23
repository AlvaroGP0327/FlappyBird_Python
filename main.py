import pygame, sys, os
from random import randint, choice
import random

pygame.init()
size = (576,1024) 
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#sounds settings
#pygame.mixer.pre_init(44100,-16,2,512)

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
        self.rect.x -= 9
    
    def destroy_pipes(self):
        if self.rect.right < 0:
            self.kill()
    
    def update(self):
        self.movement_pipe()
        self.destroy_pipes()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.down_flap = pygame.image.load('assets/redbird-downflap.png').convert_alpha() 
        self.down_flap = pygame.transform.scale2x(self.down_flap)
        self.up_flap = pygame.image.load('assets/redbird-upflap.png').convert_alpha()
        self.up_flap = pygame.transform.scale2x(self.up_flap)
        self.fly_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.fly_sound.set_volume(0.5)
        
        self.image = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(topleft=(50,512))
        
        #bird object initiate with force gravity action.
        self.gravity = 0
        self.jumping = False
    
    def gravity_force_for_bird(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if not self.jumping:
            self.image = self.up_flap
        
    def jump_bird(self):
        self.gravity = -20
        self.image = self.down_flap
        if not pygame.mixer.get_busy():
            self.fly_sound.play()

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jumping = True
            self.jump_bird()
        else:
            self.jumping = False
    
    def rotate_bird(self):
        #method for rotate a base image.
        angle = -self.gravity * 2 #positive gravity bird look to sky #negative gravity bird look to ground
        self.image = pygame.transform.rotate(self.image,angle=angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self):
        self.player_input()
        self.gravity_force_for_bird()
        self.rotate_bird()
        
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path_style_font = 'assets/fonts/04B_19.TTF' 
        self.text_font = pygame.font.Font(self.path_style_font,25)
        self.score = ""
        self.image = self.text_font.render(self.score,False,'black')
        self.rect = self.image.get_rect(topleft=(50,20))
        self.time_life_game = 0

    def measure_time(self):
        self.time_life_game = int((pygame.time.get_ticks()-start_time)/1000) 
        self.image = self.text_font.render(f"Score: {str(self.time_life_game)}",False,'black') 
    
    def update(self):
        self.measure_time()           
        

#Instances
sky = Sky()
ground = Ground()
ground_2 = Ground()
ground_2.initial_position()
bird = Bird()
score = Score()

#Sprite Groups
sky_group = pygame.sprite.GroupSingle()
sky_group.add(sky)

ground_group = pygame.sprite.Group()
ground_group.add(ground)
ground_group.add(ground_2)

player_group = pygame.sprite.GroupSingle()
player_group.add(bird)

obstacle_group = pygame.sprite.Group()
#obstacles will be added on game loop dinamically

score_group = pygame.sprite.GroupSingle()
score_group.add(score)

#Timer for create random pipes obstalces.
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1200)

pipe_gap = -300

#collison manager
def detect_collisions():
    '''Return true if bird collide with a pipe'''
    #Collisions detect
    if pygame.sprite.spritecollide(player_group.sprite,obstacle_group,False):
        #after collide remove all sprites from obstacle group
        obstacle_group.empty()
        
        return True
    else:
        return False
##collision sound efect
collisions_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

#Game control Variables.
game_active = False
start_time = 0 #declarar para medir el tiempo desde que se inicia la partida

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if game_active:
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
        else:
            #logic for restart game
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_r:
                    player_group.sprite.rect.topleft = (50,512)
                    game_active = True
                    start_time = pygame.time.get_ticks()
    
    if game_active:
    #draw and update all scenario
    #detect collisions
        ground_group.update()
        obstacle_group.update()
        sky_group.draw(screen)
        obstacle_group.draw(screen)
        ground_group.draw(screen)
        score_group.draw(screen)
        score_group.update()
        
        #draw and update player
        player_group.draw(screen)
        player_group.update()
        #print(player_group.sprite.jumping) Como acceder a un objeto sprite dentro de un grupo
        
        collisions = detect_collisions()
        if collisions:
            collisions_sound.play()
            game_active = False
    else:
        screen.fill('yellow')    
    
    pygame.display.update()
    clock.tick(60)    