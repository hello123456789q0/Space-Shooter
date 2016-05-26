import pygame

# Colors
BLUE = (0,191,255)
GREY = (125, 125, 125)
LIGHT_GREY = (200, 200, 200)
WHITE = (255, 255, 255)


# Fonts
FONT_SM = pygame.font.Font("fonts/chary.ttf", 32)
FONT_MD = pygame.font.Font("fonts/chary.ttf", 48)
FONT_LG = pygame.font.Font("fonts/chary.ttf", 64)
FONT_XL = pygame.font.Font("fonts/chary.ttf", 96)


# Images
fighter_img = pygame.image.load("img/fighter.png")
alien_img = pygame.image.load("img/bug.png")
bullet_img = pygame.image.load("img/bullet.png")
bomb_img = pygame.image.load("img/bomb.png")


# Sounds
SHOT = pygame.mixer.Sound("sounds/shot.ogg")
HIT = pygame.mixer.Sound("sounds/hit.ogg")
THEME = pygame.mixer.Sound("sounds/take_a_chance.ogg")
