from Objects import Block, BLOCK_SIZE, SuperBattery, NormalBattery, Portal, BacteriumNormal, BacteriumMutant, \
    Spike, PlusHealth, PlusJump, PlusSpeed, DarkBall, Player, Bullet, Canon
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
LEVEL_1_OBJECTS.append(Canon(position=Coord(1200, height - 180, 0), direction='l', delay = 100))
LEVEL_1_OBJECTS.append(SuperBattery(position=Coord(700, height - 210, 0)))
LEVEL_1_OBJECTS.append(SuperBattery(position=Coord(400, height - 310, 0)))
LEVEL_1_OBJECTS.append(SuperBattery(position=Coord(300, height - 200, 0)))

LEVELS.append([LEVEL_1_BLOCKS + LEVEL_1_FLOOR, LEVEL_1_OBJECTS])

del x

LEVEL_4_FLOOR = []
LEVEL_4_BLOCKS = []
LEVEL_4_OBJECTS = []
x = 0
while x < width:
    LEVEL_4_FLOOR.append(Block(Coord(x, height - BLOCK_SIZE, 0), "ground"))
    x += BLOCK_SIZE
LEVEL_4_BLOCKS.append(Block(Coord(1050, 540, 1050), 'brick'))
LEVEL_4_OBJECTS.append(PlusSpeed(position=Coord(900, height - 100, 0)))

LEVEL_4_BLOCKS.append(Block(Coord(1020, 540, 1020), 'brick'))
LEVEL_4_OBJECTS.append(PlusJump(position=Coord(1000, height - 580, 0)))
LEVEL_4_BLOCKS.append(Block(Coord(1050, 460, 1050), 'brick'))

LEVEL_4_BLOCKS.append(Block(Coord(960, 390, 960), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(870, 360, 870), 'brick'))

LEVEL_4_BLOCKS.append(Block(Coord(780, 300, 780), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(870, 240, 870), 'brick'))

LEVEL_4_BLOCKS.append(Block(Coord(930, 180, 930), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(990, 120, 990), 'brick'))
LEVEL_4_OBJECTS.append(BacteriumMutant(
    position=Coord(830, height - 510, 0)))  # daño
LEVEL_4_BLOCKS.append(Block(Coord(900, 90, 900), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(750, 150, 750), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(690, 210, 690), 'brick'))
LEVEL_4_OBJECTS.append(SuperBattery(position=Coord(700, height - 510, 0)))
LEVEL_4_OBJECTS.append(SuperBattery(position=Coord(500, height - 510, 200)))

LEVEL_4_BLOCKS.append(Block(Coord(600, 210, 600), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(510, 240, 510), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(420, 210, 420), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(360, 270, 360), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(300, 270, 300), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(210, 240, 210), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(330, 170, 330), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(360, 120, 360), 'brick'))
LEVEL_4_BLOCKS.append(Block(Coord(420, 60, 420), 'brick'))
LEVEL_4_OBJECTS.append(SuperBattery(position=Coord(500, height - 600, 0)))
LEVEL_4_OBJECTS.append(Portal(position=Coord(width - 10, height - 600, 0)))


# LEVELS.append([LEVEL_4_BLOCKS + LEVEL_4_FLOOR, LEVEL_4_OBJECTS])
