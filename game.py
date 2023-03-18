import pygame
import pygame.locals
import random

#initialise
pygame.init()

#master variables
gravity = 0.35
bird_movement = 0
display_w = 285
display_h = 510
game_on = True
score = 0
high_score = 0 
scoring_timer = 100

#Set Display Size
game_display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Flappy')

clock = pygame.time.Clock()

#Populate Pipes
pipes_list2 =[]
show_pipe = pygame.USEREVENT
pygame.time.set_timer(show_pipe, 1100)

#import sprites
background = pygame.image.load('assets/sprites/background-day.png').convert()

base = pygame.image.load('assets/sprites/base.png').convert()
base_x_pos = 0

#pipe sprites
pipes_list = ['assets/sprites/pipe/pipe-green.png','assets/sprites/pipe/pipe-red.png']
pipe_sur = pygame.image.load(random.choice(pipes_list))
pipe_heights = [200, 300, 400]

#bird image
bird_image = ['assets/sprites/bluebird-upflap.png','assets/sprites/redbird-midflap.png','assets/sprites/yellowbird-downflap.png']
bird_sur = pygame.image.load(bird_image[1]).convert_alpha()
bird_rectangle = bird_sur.get_rect(center = (25,255))

#Styling 
font = pygame.font.Font('Unique-VF.ttf',34)
game_over_sur = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
game_over_rectangle = game_over_sur.get_rect(center = (143,255))

#Audio 
flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
lose_sound = pygame.mixer.Sound('assets/audio/hit.wav')
scoring_sound = pygame.mixer.Sound('assets/audio/point.wav')
die_sound = pygame.mixer.Sound('assets/audio/die.wav')

#Movement & Pipes
def base_move():
    game_display.blit(base,(base_x_pos,435))
    game_display.blit(base,(base_x_pos +285, 435))

def adding_pipes():
    random_pipe_height = random.choice(pipe_heights)
    top_pipe = pipe_sur.get_rect(midtop = (288,random_pipe_height))
    base_pipe = pipe_sur.get_rect(midbottom = (288,random_pipe_height - 150))
    return top_pipe, base_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def show_pipes(pipes):
    for pipe in pipes:
        if pipe.top >= 0:
            game_display.blit(pipe_sur, pipe)

        else:
            reverse_pipe = pygame.transform.flip(pipe_sur, False, True)
            game_display.blit(reverse_pipe, pipe)

#Collusion
def collusion(pipes):
    for pipe in pipes:
        if bird_rectangle.colliderect(pipe):
            lose_sound.play()
            die_sound.play()
            return False  
    
    if bird_rectangle.top <= -25 or bird_rectangle.bottom >= 435:
        return False
    
    return True   

#Bird Move
def bird_rotate(bird):
    bird_flapping = pygame.transform.rotozoom(bird, bird_movement*2.5, 1)
    return bird_flapping

#Scoring
def display_score(game):
    if game == 'game_on':
        score_sur = font.render('Score: {}'.format(str(int(score))), True,(255,255,255))
        score_rectangle = score_sur.get_rect(center =(143,30))
        game_display.blit(score_sur, score_rectangle)

    elif game == 'game_over':
        score_sur = font.render('Score: {}'.format(str(int(score))), True,(255,255,255))
        score_rectangle = score_sur.get_rect(center =(143,30))
        game_display.blit(score_sur, score_rectangle)

        high_score_sur = font.render('High Score: {}'.format(str(int(high_score))), True,(255,255,255))
        High_score_rectangle = high_score_sur.get_rect(center =(143,100))
        game_display.blit(high_score_sur, High_score_rectangle)

def high_score_update(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#Game end functionality 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and (
            event.type == pygame.K_ESCAPE or
            event.type == pygame.K_q)):
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN and game_on == True:
            if event.key == pygame.K_SPACE:
                bird_sur = pygame.image.load(bird_image[0]).convert()
                bird_movement = 0
                bird_movement -= 8.5
                flap_sound.play()



        elif event.type == pygame.KEYDOWN and game_on == False:
            if event.key == pygame.K_SPACE:
                pipes_list2.clear()
                bird_rectangle.center =(25,255)
                bird_sur = pygame.image.load(bird_image[1]).convert()
                bird_movement = 0
                game_on = True

        if random.choice(pipes_list) == pipes_list[0] or pipe_sur == pygame.image.load(pipes_list[0]):
            pipe_sur = pygame.image.load(pipes_list[1])

        else:
            pipe_sur = pygame.image.load(pipes_list[1])

        if event.type == show_pipe:
            pipes_list2.extend(adding_pipes())

    clock.tick(65)
    game_display.blit(background,(0,0))


    if game_on:
        bird_movement += gravity
        bird_rectangle.centery += int(bird_movement)

        flappy = bird_rotate(bird_sur)

        game_display.blit(base,(0,435))
        game_display.blit(flappy,bird_rectangle)

        game_on = collusion(pipes_list2)
        pipes_list2 = move_pipe(pipes_list2)
        show_pipes(pipes_list2)

        score += 0.01
        display_score('game_on')
        scoring_timer -= 1
        if scoring_timer <= 0:
            scoring_sound.play()
            scoring_timer = 100
    else:
        high_score = high_score_update(score, high_score)
        display_score('game_over')
        game_display.blit(game_over_sur, game_over_rectangle)

    base_move()
    base_x_pos -= 1

    if base_x_pos >= -285:
        base_x_pos = 0


    pygame.display.update()


