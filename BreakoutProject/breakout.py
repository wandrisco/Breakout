
import pygame
import sys, os
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class BreakColors:
    BLACK = pygame.Color(0,0,0)
    WHITE = pygame.Color(255,255,255)
    BLUE = pygame.Color(0,0,255)
    RED = pygame.Color(255,0,0)

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(0,SCREEN_HEIGHT-32,160,16)

class Ball:
    def __init__(self, pos):
        self.reset(pos)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def reverseY(self):
        self.dy = -self.dy

    def reverseX(self):
        self.dx = -self.dx

    def reset(self, pos):
        self.rect = pygame.Rect(pos,SCREEN_HEIGHT-64,16,16)
        self.dx = 4
        self.dy = -4

class Block:
    def __init__(self, rect):
        self.rect = rect        

class BreakoutGame:
    def __init__(self):
        self.running = False
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.screenSize = SCREEN_WIDTH, SCREEN_HEIGHT
        pygame.display.set_caption('Breakout!')
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(self.screenSize)

        self.font = pygame.font.Font("Fonts\PressStart2P.ttf", 16)

        self.paddle = Paddle()
        self.ball = Ball(SCREEN_WIDTH/2)
        
        self.topEdge = pygame.Rect(0,0,SCREEN_WIDTH,16)
        self.leftEdge = pygame.Rect(0,0,16,SCREEN_HEIGHT)
        self.rightEdge = pygame.Rect(SCREEN_WIDTH-16,0,16,SCREEN_HEIGHT)

        self.boopSound = pygame.mixer.Sound('Sounds/Blip1.wav')
        self.bloopSound = pygame.mixer.Sound('Sounds/Blip2.wav')
        self.explosionSound = pygame.mixer.Sound('Sounds/Explosion.wav')

        self.lives = 3
        self.score = 0
        self.level = 1
		


        self.blocks = [pygame.Rect((SCREEN_WIDTH/6*x)+21,(SCREEN_HEIGHT/8*y)+32,64,16) for x in range(6) for y in range(4)]
        
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                if event.type == MOUSEMOTION:
                    # update the paddle postition to the mouse position
                    self.mousePosition = event.pos[0]
                    self.paddle.rect.x = self.mousePosition - (self.paddle.rect.width / 2)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.tick()
            self.render()
            pygame.display.update()
            self.clock.tick(60)

    def tick(self):
        # update the ball postition
        self.ball.update()

        # check for collisions with edges
        if self.ball.rect.left <= self.leftEdge.right:
            self.boopSound.play()
            self.ball.reverseX()
        elif self.ball.rect.right >= self.rightEdge.left:
            self.boopSound.play()
            self.ball.reverseX()
        if self.ball.rect.top <= self.topEdge.bottom:
            self.boopSound.play()
            self.ball.reverseY()

        # check for collision with paddle
        if self.ball.rect.bottom >= self.paddle.rect.top and self.ball.rect.bottom <= SCREEN_HEIGHT and self.ball.rect.centerx in range(self.paddle.rect.left,self.paddle.rect.right):
            self.ball.rect.bottom = self.paddle.rect.top
            self.bloopSound.play()
            self.ball.reverseY()

        # check for collision with block
        collisionIndex = self.ball.rect.collidelist(self.blocks)
        if collisionIndex != -1:
            self.ball.reverseY()
            self.blocks.pop(collisionIndex)
            self.explosionSound.play()
            self.score += 100
            

        # check for out
        if self.ball.rect.top >= SCREEN_HEIGHT:
            self.lives -= 1
            self.ball.reset(self.paddle.rect.x + (self.paddle.rect.width/2))

        # check for paddle out
        if self.paddle.rect.left <= self.leftEdge.right:
            self.paddle.rect.left = self.leftEdge.right
        elif self.paddle.rect.right >= self.rightEdge.left:
            self.paddle.rect.right = self.rightEdge.left

        # check for dead
        if self.lives <= 0:
            self.gameOver()

        # check for won
        if len(self.blocks) <= 0:
            self.win()

    def render(self):
        #print('rendering...') # for testing rendering
        # clear the screen
        self.screen.fill(BreakColors.WHITE)

        self.background = pygame.image.load(os.path.join('pieces','background.jpg'))
        self.screen.blit(self.background, (0,0))
        # flip the display so the background is on there
        # draw edges
          #Top
        pygame.draw.rect(self.screen, BreakColors.BLACK, self.topEdge)
          #Left
        pygame.draw.rect(self.screen, BreakColors.BLACK, self.leftEdge)
          #Top
        pygame.draw.rect(self.screen, BreakColors.BLACK, self.rightEdge)
 
        # draw the paddle
        pygame.draw.rect(self.screen, BreakColors.BLACK, self.paddle.rect)

        # draw the ball
        pygame.draw.rect(self.screen, BreakColors.BLACK, self.ball.rect)

        # draw blocks
        for block in self.blocks:
            pygame.draw.rect(self.screen, BreakColors.BLUE, block)

        # draw scoreboard
        scoreSurface = self.font.render("Lives: %i   Score: %i   Level: %i" % (self.lives,self.score,self.level), False, BreakColors.RED)
        self.screen.blit(scoreSurface, (16,16))

    def gameOver(self):
        messageSurface = self.font.render("GAME OVER!", False, BreakColors.RED)
        text_rect = messageSurface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(messageSurface, text_rect)
        pygame.display.update()
        pygame.time.wait(1000)
        self.level = 0
        self.score = 0
        self.resetGame()

    def win(self):
        messageSurface = self.font.render("CONGRATULATIONS!", False, BreakColors.RED)
        text_rect = messageSurface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(messageSurface, text_rect)
        pygame.display.update()
        pygame.time.wait(1000)
        self.level += 1
        self.resetGame()

    def resetGame(self):
        self.lives = 3
        self.ball.reset(SCREEN_WIDTH/2)
        self.blocks = [pygame.Rect((SCREEN_WIDTH/6*x)+21,(SCREEN_HEIGHT/8*y)+32,64,16) for x in range(6) for y in range(4)]
        
if __name__ == "__main__":
    game = BreakoutGame()
    game.run()
