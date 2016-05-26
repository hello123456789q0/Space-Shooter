# Import pygame
import pygame


# Initialize game engine
pygame.init()


# More imports
import os
import random
from assets import *
from sprites import Cannon, Alien, Ground
from scenery import Mountains, Stars


# Stages
START = 0
PLAYING = 1
PAUSED = 2
DELAY = 3
GAME_OVER = 4


# Window settings
TITLE = "Alien vs Spaceship"
WIDTH = 1000
HEIGHT = 660


# Play settings
cannon_speed = 4
bullet_speed = 7
bomb_speed = 5
drop_amount = 12

initial_shot_limit = 3
initial_alien_speed = 2
initial_bomb_rate = 5

sound_on = True


# Data settings
score_file = "data/high_score.txt"
default_high_score = 1


# Make window
os.environ['SDL_VIDEO_WINDOW_POS'] = "15, 30:"
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)


# Hide mouse cursor over screen
pygame.mouse.set_visible(0)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60
delay_ticks = 45


# Define functions
def read_high_score():
    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            return max([int(f.read().strip()), default_high_score])
    else:
        return default_high_score

def save_high_score(score):
    if not os.path.exists('data'):
        os.mkdir('data')

    with open((score_file), 'w') as f:
        f.write(str(score))

def start():
    global cannon, alien_speed, bomb_rate, shot_limit, score, level, stage

    cannon = Cannon(480, 540)
    alien_speed = initial_alien_speed
    bomb_rate = initial_bomb_rate
    shot_limit = initial_shot_limit

    score = 0
    level = 1
    stage = START

def setup():
    global aliens, bombs, bullets, stage, ticks

    a1 = Alien(-400, 90, alien_speed)
    a2 = Alien(500, 90, alien_speed)
    a3 = Alien(600, 90, alien_speed)
    a4 = Alien(500, 150, alien_speed)
    a5 = Alien(400, 150, alien_speed)
    a6 = Alien(600, 150, alien_speed)
    aliens = [a1, a2, a3, a4, a5, a6]
    
    bombs = []
    bullets = []

    ticks = delay_ticks
    stage = DELAY

def advance():
    global level, alien_speed, bomb_rate

    level += 1
    alien_speed += 0.5
    bomb_rate += 1

    setup()

def end_game():
    global stage

    stage = GAME_OVER

def display_start_screen(screen, high_score):

    title_text = FONT_XL.render(TITLE, True, WHITE)
    sample_text = FONT_SM.render("Press SPACE to play", True, WHITE)

    screen.blit(title_text, [WIDTH // 2 - title_text.get_rect().width // 2 , 200])
    screen.blit(sample_text, [WIDTH // 2 - sample_text.get_rect().width // 2 , 300])

def display_pause_screen(screen):
    title_text = FONT_XL.render("Paused", True, WHITE)
    sample_text = FONT_SM.render("Press P to unpause the game", True, WHITE)

    screen.blit(title_text, [WIDTH // 2 - title_text.get_rect().width // 2 , 200])
    screen.blit(sample_text, [WIDTH // 2 - sample_text.get_rect().width // 2 , 300]) 



def display_end_screen(screen):
    title_text = FONT_XL.render("Game Over", True, WHITE)
    sample_text = FONT_SM.render("Press SPACEBAR to restart", True, WHITE)

    screen.blit(title_text, [WIDTH // 2 - title_text.get_rect().width // 2 , 200])
    screen.blit(sample_text, [WIDTH // 2 - sample_text.get_rect().width // 2 , 300])

def display_stats(screen, score, level, high_score, shield):
   score_text = FONT_SM.render("Score: " + str(score), True, WHITE)
   highscore_text = FONT_SM.render("High score: " + str(high_score), True, WHITE)
   shield_text = FONT_SM.render("Shield: " + str(shield), True, WHITE)
   level_text = FONT_SM.render("Level: " + str(level), True, WHITE)
   screen.blit(shield_text, [10, 600])
   screen.blit(score_text, [WIDTH // 2  - score_text.get_rect().width // 2, 10])
   screen.blit(highscore_text, [10, 10])
   screen.blit(level_text, [850, 600])


# Make scenery objects
ground = Ground(0, 560, 1000, 5)
mountains = Mountains(0, 480, 1000, 80, 9)
stars = Stars(0, 0, 1000, 560, 125)


# Get high score
high_score = read_high_score()


# Game loop
done = False
start()

while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    setup()

            elif stage == PLAYING:
                if event.key == pygame.K_SPACE and len(bullets) < shot_limit:
                    SHOT.play()
                    cannon.shoot(bullets, -bullet_speed)
                    score -= 1

                elif event.key == pygame.K_p:
                    stage = PAUSED

            elif stage == PAUSED:
                if event.key == pygame.K_p:
                    stage = PLAYING

            elif stage == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    start()

    if stage == PLAYING:
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            cannon.vx = cannon_speed
        elif key[pygame.K_LEFT]:
            cannon.vx = -cannon_speed
        else:
            cannon.vx = 0


    # Game logic
    if stage == DELAY:
        if ticks > 0:
            ticks -= 1
        else:
            stage = PLAYING

    if stage == PLAYING:
        if score > high_score:
            high_score = score
            
        # process scenery
        stars.update()

        # process cannon
        cannon.update()

        # process enemies
        fleet_hits_edge = False

        for a in aliens:
            a.update()

            r = random.randint(0, 1000)
            if r < bomb_rate:
                a.drop_bomb(bombs, bomb_speed)

            if a.x <= 0 or a.x + a.w >= WIDTH:
                fleet_hits_edge = True

        if fleet_hits_edge:
            for a in aliens:
                a.reverse_and_drop(drop_amount)

        # process bombs
        for b in bombs:
            b.update()

            if b.intersects(cannon):
                b.kill()
                cannon.apply_damage(20)
            elif b.intersects(ground):
                b.kill()

        # process bullets
        for b in bullets:
            b.update()

            for a in aliens:
                if b.intersects(a):
                    b.kill()
                    a.kill()
                    score += a.value

            if b.y + b.h < 0:
                b.kill()

        # check game status
        if cannon.alive == False:
            end_game()
        elif len(aliens) == 0:
            advance()


    # Drawing code
    screen.fill(BLUE)

    if stage == START:
        display_start_screen(screen, high_score)

    elif stage in [PLAYING, PAUSED, DELAY, GAME_OVER]:
        stars.draw(screen)
        mountains.draw(screen)
        ground.draw(screen)

        cannon.draw(screen)

        for a in aliens:
            a.draw(screen)

        for b in bullets:
            b.draw(screen)

        for b in bombs:
            b.draw(screen)

        if stage == PAUSED:
            display_pause_screen(screen)
        if stage == GAME_OVER:
            display_end_screen(screen)

        display_stats(screen, score, level, high_score, cannon.shield)


    # Update screen
    pygame.display.flip()
    clock.tick(refresh_rate)


    # Remove killed objects
    if stage != START:
        aliens = [a for a in aliens if a.alive]
        bullets = [b for b in bullets if b.alive]
        bombs = [b for b in bombs if b.alive]


# Close window on quit
pygame.quit()
