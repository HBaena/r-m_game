from Objects import Block, BLOCK_SIZE, SuperBattery, NormalBattery, Saw, Portal, BacteriumNormal, BacteriumMutant, \
    Spike, PlusHealth, PlusJump, PlusSpeed, DarkBall, Player
from Miscellaneous import Coord
# from main import  width, height
import pygame

MORTY = Player('morty', Coord(100, 0, 0), [8, 0], 30, 10, 2, 2, 50)
size = width, height = 1480, 700
pygame.init()

'''
    LEVEL 1 Objects
'''
LEVELS = []

LEVEL_1_FLOOR = []
LEVEL_1_BLOCKS = []
LEVEL_1_OBJECTS = []
x = 0
while x < width:
    LEVEL_1_FLOOR.append(Block(Coord(x, height - BLOCK_SIZE, 0), "ground"))
    x += BLOCK_SIZE
# LEVEL_1_BLOCKS.append(Block(Coord(500, 0, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(100, 100, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(150, 150, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(200, 200, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(300, 250, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(400, 300, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(500, 400, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(600, 500, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(700, 600, 0), 'brick'))
LEVEL_1_BLOCKS.append(Block(Coord(700, 630, 0), 'brick'))

LEVEL_1_OBJECTS.append(Spike(Coord(500, height - 100, 0)))
LEVEL_1_OBJECTS.append(SuperBattery(position=Coord(550, height - 100, 0)))
LEVEL_1_OBJECTS.append(BacteriumNormal(position=Coord(750, height - 100, 0)))
LEVEL_1_OBJECTS.append(BacteriumMutant(position=Coord(650, height - 100, 0)))
LEVEL_1_OBJECTS.append(NormalBattery(position=Coord(600, height - 100, 0)))
LEVEL_1_OBJECTS.append(SuperBattery(position=Coord(800, height - 100, 0)))
LEVEL_1_OBJECTS.append(PlusHealth(position=Coord(850, height - 100, 0)))
LEVEL_1_OBJECTS.append(PlusSpeed(position=Coord(900, height - 100, 0)))
LEVEL_1_OBJECTS.append(PlusJump(position=Coord(950, height - 100, 0)))
LEVEL_1_OBJECTS.append(DarkBall(position=Coord(950, height - 100, 0)))
# LEVEL_1_OBJECTS.append(Saw(position=Coord(800, height - 100, 0)))
LEVEL_1_OBJECTS.append(Portal(position=Coord(1200, height - 180, 0)))

LEVELS.append([LEVEL_1_BLOCKS + LEVEL_1_FLOOR, LEVEL_1_OBJECTS])

del x
LEVEL_2_FLOOR = []
LEVEL_2_BLOCKS = []
LEVEL_2_OBJECTS = []
x = 0
while x < width:
    LEVEL_2_FLOOR.append(Block(Coord(x, height - BLOCK_SIZE, 0), "ground"))
    x += BLOCK_SIZE
LEVEL_2_BLOCKS.append(Block(Coord(500, 540, 500), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(400, 500, 400), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(600, 500, 600), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(400, 360, 400), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(600, 360, 600), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(700, 440, 700), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(300, 440, 200), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(500, 300, 500), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(600, 230, 600), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(700, 160, 130), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(500, 160, 130), 'brick'))
LEVEL_2_BLOCKS.append(Block(Coord(600, 100, 600), 'brick'))


LEVEL_2_OBJECTS.append(Spike(Coord(500, height - 100, 0)))
# LEVEL_1_OBJECTS.append(Battery(position=Coord(800, height - 100, 0), charge=1))
LEVEL_2_OBJECTS.append(NormalBattery(position=Coord(800, height - 100, 0)))

del x
