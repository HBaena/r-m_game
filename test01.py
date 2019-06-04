import pygame
import sys
import threading
from Objects import Player
from Miscellaneous import Coord
from Objects import Block
KEY_CLICK_DOWN = 2
KEY_CLICK_UP = 3
KEY_UP = 273
KEY_DOWN = 274
KEY_RIGHT = 275
KEY_LEFT = 276
BLOCK_SIZE = 30
PLAYER_SCALE = 0.5

K_UP = 0
K_DOWN = 1
K_RIGHT = 2
K_LEFT = 3
K_RSHIFT = 4
K_LSHIFT = 5
K_SPACE = 6

USED_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT,
             pygame.K_LEFT, pygame.K_RSHIFT, pygame.K_LSHIFT,
             pygame.K_SPACE]

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        print(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class SimpleThread (threading.Thread):
    def __init__(self, fun, keys, left_edge, right_edge,
                 rect):
        threading.Thread.__init__(self)
        fun(keys, left_edge, right_edge, rect)

class RefreshScreen(threading.Thread):
    """docstring for RefreshScreen"""
    def __init__(self, screen, objects):
        threading.Thread.__init__(self)
        # Refresh screen objects
        for obj in objects:
            screen.blit(obj.asset, obj.bounding)

class RefreshBackground(threading.Thread):
    """docstring for RefreshScreen"""
    def __init__(self, screen, background):
        threading.Thread.__init__(self)
        screen.blit(background.image, background.rect)
        


if __name__ == "__main__":
    # Init all pygame modules
    pygame.init()
    # size of the window
    size = width, height = 1080, 655
    speed = [1, 0]
    black = 0, 0, 0
    floor = []
    blocks = []
    # background = pygame.image.load('sprites/scenes/scene_02.jpg').convert_alpha()
    screen = pygame.display.set_mode(size)
    background = Background('sprites/scenes/scene_02.jpg', [0,0])
    player_morty = Player("rick",
                          Coord(100, 0, 0), [8, 0], 30, 10, 2, 2, 50)
    print(player_morty.bounding)
    x = 0
    player_morty.detect__vertical_collisions(floor + blocks)

    while x < width:
        floor.append(Block(Coord(x, height - BLOCK_SIZE, 0), "ground"))
        x += BLOCK_SIZE

    blocks.append(Block(Coord(500, 0, 0), 'brick'))
    blocks.append(Block(Coord(100, 100, 0), 'brick'))
    blocks.append(Block(Coord(150, 150, 0), 'brick'))
    blocks.append(Block(Coord(200, 200, 0), 'brick'))
    blocks.append(Block(Coord(300, 250, 0), 'brick'))
    blocks.append(Block(Coord(400, 300, 0), 'brick'))
    blocks.append(Block(Coord(500, 400, 0), 'brick'))
    blocks.append(Block(Coord(600, 500, 0), 'brick'))
    blocks.append(Block(Coord(700, 600, 0), 'brick'))
    blocks.append(Block(Coord(700, 630, 0), 'brick'))
    blocks.append(Block(Coord(700, 570, 0), 'brick'))
    rects = []
    for block in blocks:
        rects.append(block.bounding)

    screen.fill([255, 255, 255])
    screen.blit(background.image, background.rect)
    while 1:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                sys.exit()
        keys = []
        for i in USED_KEYS:
            keys.append(pygame.key.get_pressed()[i])

        # Movement
        player_morty.change_movement_y(keys[K_SPACE], floor + blocks, 0, 0)
        try:
            # background.rect = pygame.Rect(player_morty.bounding)
            SimpleThread(player_morty.change_movement_x,
                         keys, 0, width, floor + blocks)

        except Exception as e:
            raise e
        # 
        try:
            RefreshBackground(screen, background)
        except Exception as e:
            raise e
        try:
            # screen.blit(background.image, background.rect)
            # screen.fill([255, 255, 255])
            RefreshScreen(screen, [player_morty] + blocks + floor)
        except Exception as e:
            raise e

        pygame.display.update()
        pygame.display.flip()
