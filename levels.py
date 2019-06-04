from Objects import Block, BLOCK_SIZE, Obtainable
from Miscellaneous import Coord
import pygame
size = width, height = 1080, 655
pygame.init()

'''
    LEVEL 1 Objects
'''
LEVEL_1_FLOOR = []
LEVEL_1_BLOCKS = []
LEVEL_1_OBJECTS = []
x = 0
while x < width:
    LEVEL_1_FLOOR.append(Block(Coord(x, height - BLOCK_SIZE, 0), "ground"))
    x += BLOCK_SIZE
LEVEL_1_BLOCKS.append(Block(Coord(500, 0, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(100, 100, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(150, 150, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(200, 200, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(300, 250, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(400, 300, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(500, 400, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(600, 500, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(700, 600, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(700, 630, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(700, 570, 0), 'brick'))

LEVEL_1_OBJECTS.append(Obtainable(Coord(500, height - 100, 0), 'sprites/block/spikes.png', name="spike"))

del x