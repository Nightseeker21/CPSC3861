import pygame
import sys
from pygame.locals import *
from random import randint

# Setting up pygame, color, window, and images
pygame.init()
mainClock = pygame.time.Clock()

#Set up for the window size and colors
WINDOWWIDTH = 980
WINDOWHEIGHT = 464
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (16, 78, 139)
RED = (139, 26, 26)
TEXTCOLOR = (0, 0, 0)
BACKGROUND = (72, 118, 255)
Surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong by Therese Lim')
font = pygame.font.SysFont(None, 48)

#Variables
FPS = 60
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
ROUNDS = 5
MUST_WIN_3 = 3

# Setting up images
BACKGROUND_IMAGE = pygame.image.load('Images/background.png')
rect0 = BACKGROUND_IMAGE.get_rect()
SPHERE = pygame.image.load('Images/sphere.png')
rect1 = SPHERE.get_rect()
PADDLE = pygame.image.load('Images/paddle_design.jpg')
rect2 = PADDLE.get_rect()

#Creating text for the game
def drawText(text, font, surf, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surf.blit(textobj, textrect)

#Terminate the game
def terminate():
    pygame.quit()
    sys.exit()

#Function for player to press any key
def PlayerPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

#Collision
def checkEdgeCollision(ball, ballDirx, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirx = ballDirx * -1
    return ballDirx, ballDirY

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400

    def moveRight(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 483:
            self.rect.x = 483

    def moveLeft(self, pixels):
        self.rect.x += pixels
        if self.rect.x > 890:
            self.rect.x = 890

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.circle(self.image, color, [0, 0], width, height)

        self.velocity = [randint(4,8), randint(-8,8)]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)

player_paddle = Paddle(BLUE, 10, 100)
player_paddle.rect.x = 970
player_paddle.rect.y = 200

player_paddle2 = Paddle(BLUE, 100, 10)
player_paddle2.rect.x = 700
player_paddle2.rect.y = 0

player_paddle3 = Paddle(BLUE, 100, 10)
player_paddle3.rect.x = 700
player_paddle3.rect.y = 455

AI_paddle = Paddle(RED, 10, 100)
AI_paddle.rect.x = 0
AI_paddle.rect.y = 200

AI_paddle2 = Paddle(RED, 100, 10)
AI_paddle2.rect.x = 200
AI_paddle2.rect.y = 0

AI_paddle3 = Paddle(RED, 100, 10)
AI_paddle3.rect.x = 199
AI_paddle3.rect.y = 455

ball = Ball(WHITE, 10, 10)
ball.rect.x = 100
ball.rect.y = 460

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(player_paddle)
all_sprites_list.add(player_paddle2)
all_sprites_list.add(player_paddle3)
all_sprites_list.add(AI_paddle)
all_sprites_list.add(AI_paddle2)
all_sprites_list.add(AI_paddle3)
all_sprites_list.add(ball)

def play():
    # Setting up sounds
    game_over_sound = pygame.mixer.Sound('Sounds/game_over.wav')
    ball_hit = pygame.mixer.Sound('Sounds/ball_sound.wav')

    #Start Screen
    Surface.fill(BACKGROUND)
    drawText('Pong', font, Surface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press any key to play', font, Surface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    PlayerPressKey()

    game_on = True

    player_score = 0
    AI_score = 0
    winning_score = 1

    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_on = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.moveUp(5)
        if keys[pygame.K_DOWN]:
            player_paddle.moveDown(5)
        if keys[pygame.K_LEFT]:
            player_paddle2.moveRight(5)
        if keys[pygame.K_RIGHT]:
            player_paddle2.moveLeft(5)
        if keys[pygame.K_LEFT]:
            player_paddle3.moveRight(5)
        if keys[pygame.K_RIGHT]:
            player_paddle3.moveLeft(5)

        all_sprites_list.update()

        if ball.rect.x >= 990:
            AI_score += 1
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            player_score += 1
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > 490:
            player_score += 1
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            AI_score += 1
            ball.velocity[1] = -ball.velocity[1]


        if pygame.sprite.collide_mask(ball, player_paddle) or pygame.sprite.collide_mask(ball, AI_paddle):
            pygame.mixer.music.stop()
            ball_hit.play()
            ball.bounce()

        if pygame.sprite.collide_mask(ball, player_paddle2) or pygame.sprite.collide_mask(ball, AI_paddle2):
            pygame.mixer.music.stop()
            ball_hit.play()
            ball.bounce()

        if pygame.sprite.collide_mask(ball, player_paddle3) or pygame.sprite.collide_mask(ball, AI_paddle3):
            pygame.mixer.music.stop()
            ball_hit.play()
            ball.bounce()

        Surface.fill(BACKGROUND)

        pygame.draw.line(Surface, WHITE, [WINDOWWIDTH / 2, 0], [WINDOWWIDTH / 2, WINDOWHEIGHT], 1)

        all_sprites_list.draw(Surface)

        drawText('Player Score: %s' % (player_score), font, Surface, 725, 0)
        drawText('AI Score: %s' % (AI_score), font, Surface, 10, 0)

        pygame.display.update()

        if player_score > winning_score:
            drawText('You Win!', font, Surface, WINDOWWIDTH / 3, WINDOWHEIGHT / 3)
        else:
            if AI_score > winning_score:
                break

        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    game_over_sound.play()

    drawText('AI Wins!', font, Surface, WINDOWWIDTH / 3, WINDOWHEIGHT / 3)
    drawText('Press any key to play again.', font, Surface, WINDOWWIDTH / 3 - 80, WINDOWHEIGHT / 3 + 50)

    pygame.display.update()
    PlayerPressKey()

    pygame.display.update()
    mainClock.tick(40)

play()















