
import pygame
import random
from pygame.locals import *

class Block:
    def __init__(self, rect):
        self.rect = rect
        self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Level:
	def __init__(self):
		self.blocks = []
		self.paddleWidth = 160

	def addBlock(self, x, y, w, h, r, g, b):
		block = Block(pygame.Rect(x, y, w, h))
		block.color = pygame.Color(r, g, b)
		self.blocks.append(block)


levels = []

one = Level()
numCol = 10
blockWidth = (640 - 64) / numCol
padding = 5
for x in range(numCol):
	one.addBlock(32 + x*(blockWidth+padding), 20, blockWidth - 2*padding, 20, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
levels.append(one)

#final boss
boss = Level()
boss.addBlock(0, 0, 128, 128, 255, 0, 0)
levels.append(boss);
