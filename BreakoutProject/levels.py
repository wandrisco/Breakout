

import colorsys
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

numCol = 9
blockWidth = (640 - 64) / numCol
padding = 5
for x in range(numCol):
	one.addBlock(32 + x*(blockWidth+padding), 20, blockWidth - 2*padding, 20, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#levels.append(one);

cross = Level()
cross.addBlock(150, 70, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(200, 110, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(250, 150, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(300, 190, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(350, 230, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(400, 270, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(450, 310, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

cross.addBlock(175, 90, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(225, 130, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(275, 170, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(325, 210, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(375, 250, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(425, 290, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

cross.addBlock(150, 310, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(200, 270, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(250, 230, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(300, 190, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(350, 150, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(400, 110, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(450, 70, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

cross.addBlock(175, 290, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(225, 250, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(275, 210, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(325, 170, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(375, 130, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(425, 90, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


cross.addBlock(50, 200, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(550, 200, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(300, 70, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
cross.addBlock(300, 310, 50, 30, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


#levels.append(cross);


#final boss
boss = Level()
for layer in range(9):
   bossSize = 16 * layer
   z = layer / 8.0
   r,g,b = colorsys.hsv_to_rgb(z, 1, 1)
   boss.addBlock(640/2-bossSize/2, 480/2-bossSize/2, bossSize, bossSize, int(r*255), int(g*255), int(b*255))

levels.append(boss)
