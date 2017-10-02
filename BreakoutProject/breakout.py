import pygame
import sys, os
import random
import levels
from levels import Block
from pygame.locals import *
import colorsys
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class BreakColors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    BLUE = pygame.Color(0, 0, 255)
    RED = pygame.Color(255, 0, 0)
    CYAN = pygame.Color(224, 255, 255)
    LAWNGREEN = pygame.Color(124, 252, 0)
    DARKGRAY = pygame.Color(10, 10, 10)


class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - 32, 160, 16)


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
        self.rect = pygame.Rect(pos, SCREEN_HEIGHT - 64, 20, 20)
        self.dx = 4
        self.dy = -4


class BreakoutGame:
    def __init__(self):
        self.running = False
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screenSize = SCREEN_WIDTH, SCREEN_HEIGHT
        pygame.display.set_caption('Breakout!')
        pygame.mouse.set_visible(False)
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.windowSurf = pygame.display.set_mode(self.screenSize)

        self.font = pygame.font.Font("Fonts/PressStart2P.ttf", 16)

        self.paddle = Paddle()
        self.ball = Ball(SCREEN_WIDTH / 2)

        self.topEdge = pygame.Rect(0, 0, SCREEN_WIDTH, 16)
        self.leftEdge = pygame.Rect(0, 0, 16, SCREEN_HEIGHT)
        self.rightEdge = pygame.Rect(SCREEN_WIDTH - 16, 0, 16, SCREEN_HEIGHT)

        self.boopSound = pygame.mixer.Sound('Sounds/Blip1.wav')
        self.bloopSound = pygame.mixer.Sound('Sounds/Blip2.wav')
        self.explosionSound = pygame.mixer.Sound('Sounds/Explosion.wav')
        self.music = pygame.mixer.Sound('Sounds/music.ogg')
		
        self.score = 0
        self.ballList = []
        self.colorRot = 0.0
        self.velocityX = 0
        self.lastPaddleRect = self.paddle.rect.copy()
        self.maxVelocity = 16
        self.maxVelocityChange = 8
        self.screenOffsetX = 0
        self.screenOffsetY = 0

    def run(self):
        self.running = True
        self.loadLevel(0)
        self.music.play()
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                if event.type == MOUSEMOTION:
                    # update the paddle postition to the mouse position
                    self.mousePosition = event.pos[0]
                    self.mouseRect = Rect(event.pos[0]-4, event.pos[1]-4, 8, 8)
                    self.paddle.rect.x = self.mousePosition - (self.paddle.rect.width / 2)
                    self.velocityX = self.paddle.rect.x - self.lastPaddleRect.x
                    self.lastPaddleRect = self.paddle.rect.copy()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.tick()
            self.render()
            pygame.display.update()
            self.clock.tick(60)
            self.colorRot = self.colorRot + 0.05

    def tick(self):
        # update the ball postition
        self.ball.update()
        self.ballList.append(self.ball.rect.copy())
        if len(self.ballList) > 10:
            self.ballList.pop(0)

        # check for collisions with edges
        if self.ball.rect.left <= self.leftEdge.right:
            self.ball.rect.left = self.leftEdge.right
            self.boopSound.play()
            self.screenOffsetX = self.ball.dx
            self.ball.reverseX()
        elif self.ball.rect.right >= self.rightEdge.left:
            self.ball.rect.right = self.rightEdge.left
            self.screenOffsetX = self.ball.dx
            self.boopSound.play()
            self.ball.reverseX()
        if self.ball.rect.top <= self.topEdge.bottom:
            self.ball.rect.top = self.topEdge.bottom
            self.boopSound.play()
            self.screenOffsetY = self.ball.dy
            self.ball.reverseY()

        # check for collision with paddle
        if self.ball.rect.bottom >= self.paddle.rect.top and self.ball.rect.bottom <= SCREEN_HEIGHT and self.ball.rect.centerx in range(
                self.paddle.rect.left, self.paddle.rect.right) and self.ball.rect.centery < self.paddle.rect.centery:
            self.ball.rect.bottom = self.paddle.rect.top
            self.bloopSound.play()
            self.ball.reverseY()
            spin = max(-self.maxVelocityChange, min(self.maxVelocityChange, self.velocityX))
            self.ball.dx = max(-self.maxVelocity, min(self.maxVelocity, self.ball.dx+spin))

        # check for collision with block
        for block in self.blocks:
            if self.ball.rect.colliderect(block.rect):
                overlappingArea = self.ball.rect.clip(block.rect)
                if overlappingArea.width > overlappingArea.height:
                    self.ball.reverseY()
                elif overlappingArea.height > overlappingArea.width:
                    self.ball.reverseX()
                else:
                    self.ball.reverseX()
                    self.ball.reverseY()
                self.blocks.remove(block)
                self.explosionSound.play()
                self.score += 100
                break

        # check for out
        if self.ball.rect.top >= SCREEN_HEIGHT:
            self.lives -= 1
            self.ball.reset(self.paddle.rect.x + (self.paddle.rect.width / 2))

        # check for paddle out
        if self.paddle.rect.left <= self.leftEdge.right:
            self.paddle.rect.left = self.leftEdge.right
        elif self.paddle.rect.right >= self.rightEdge.left:
            self.paddle.rect.right = self.rightEdge.left
        
        self.screenOffsetX *= 0.9
        self.screenOffsetX *= 0.9


        # check for dead
        if self.lives <= 0:
            self.gameOver()

        # check for won
        if len(self.blocks) <= 0:
            self.win()

    def render(self):
        # print('rendering...') # for testing rendering
        # clear the screen
        self.screen.fill(BreakColors.DARKGRAY)
        #self.background = pygame.image.load(os.path.join('pieces','background.jpg'))
        #self.screen.blit(self.background, (0,0))

        # draw edges
        # Top
        pygame.draw.rect(self.screen, BreakColors.BLACK, self.topEdge)
        # Left
        pygame.draw.rect(self.screen, BreakColors.BLACK, self.leftEdge)
        # Right
        pygame.draw.rect(self.screen, BreakColors.BLACK, self.rightEdge)

        # draw the paddle
        pygame.draw.rect(self.screen, BreakColors.LAWNGREEN, self.paddle.rect)
        pygame.draw.rect(self.screen, BreakColors.WHITE, self.mouseRect)

        # draw the ball
        if self.ball.dx * self.ball.dx + self.ball.dy * self.ball.dy > 32:
            z = 0
            for ballHistory in self.ballList:
                z = z + 1
                r,g,b = colorsys.hsv_to_rgb(self.colorRot + z*0.1, 1, 1)
                pygame.draw.rect(self.screen, pygame.Color(int(r*255), int(g*255), int(b*255)), ballHistory)
        
        pygame.draw.rect(self.screen, pygame.Color(255, 255, 255), self.ball.rect)

        # draw blocks
        for block in self.blocks:
            pygame.draw.rect(self.screen, block.color, block)
        self.windowSurf.blit(self.screen, (self.screenOffsetX, self.screenOffsetY))			

        # draw scoreboard
        scoreSurface = self.font.render("Lives: %i   Score: %i   Level: %i" % (self.lives, self.score, self.level + 1),
                                        False, BreakColors.WHITE)
        self.windowSurf.blit(scoreSurface, (48, 16))

    def gameOver(self):
        messageSurface = self.font.render("Game Over!", False, BreakColors.RED)
        text_rect = messageSurface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.windowSurf.blit(messageSurface, text_rect)
        pygame.display.update()
        pygame.time.wait(1000)
        self.level = 0
        self.score = 0
        self.resetGame()

    def win(self):
        messageSurface = self.font.render("CONGRATULATIONS!", False, BreakColors.LAWNGREEN)
        text_rect = messageSurface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.windowSurf.blit(messageSurface, text_rect)
        pygame.display.update()
        pygame.time.wait(1000)
        self.level += 1
        self.resetGame()
        
    def loadLevel(self, levelNum):
        self.lives = 8
        self.level = levelNum
        self.blocks = levels.levels[levelNum].blocks
        self.ball.rect = pygame.Rect(self.paddle.rect.x + (self.paddle.rect.width / 2), SCREEN_HEIGHT - 64, 20, 20)

    def resetGame(self):
        self.lives = 8
        self.loadLevel(self.level)


if __name__ == "__main__":
    game = BreakoutGame()
    game.run()
