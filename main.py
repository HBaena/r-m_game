import pygame
import sys
import threading
import levels
from Objects import Player, MAX_LIFES
from Miscellaneous import Coord
from Objects import Block, Obtainable

BLOCK_SIZE = 30
PLAYER_SCALE = 0.5
K_SPACE = 6

USED_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT,
             pygame.K_LEFT, pygame.K_RSHIFT, pygame.K_LSHIFT,
             pygame.K_SPACE]


def listen_for_exit():
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            sys.exit()


def get_keys_clicked():
    keys = []
    for i in USED_KEYS:
        keys.append(pygame.key.get_pressed()[i])
    return keys


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        print(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class SimpleThread(threading.Thread):
    def __init__(self, fun, keys, left_edge, right_edge,
                 rect, objs):
        threading.Thread.__init__(self)
        fun(keys, left_edge, right_edge, rect, objs)


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


class Level:

    def __init__(self, screen, background, blocks, objects, player, label):
        self.label = label
        self.screen = screen
        self.blocks = blocks
        self.objects = objects
        self.background = background
        self.player = player
        self.tmp = None

    def run(self, keys):
        self.change_movement(keys)
        self.refresh_screen()

    def change_movement(self, keys):
        self.tmp = self.player.bounding
        self.player.change_movement_y(keys[K_SPACE], self.blocks, 0, 0)
        SimpleThread(self.player.change_movement_x,
                     keys, 0, self.screen.get_width(), self.blocks, self.objects)

    def refresh_screen(self):
        # RefreshBackground(self.screen, self.background)
        # self.screen.fill([0, 0, 0])
        pygame.draw.rect(self.screen, [255, 255, 255],
                         pygame.Rect(self.player.bounding.x - 10, self.player.bounding.y - 10,
                                     self.player.bounding.width + 20,
                                     self.player.bounding.height + 20), 0)

        RefreshScreen(self.screen, [self.player] + self.blocks + self.objects)
        screen.blit(self.label, (10, 10))
        i = 0
        while i < int(self.player.lifes):
            screen.blit(pygame.image.load("sprites/others/heart_2.png"), (200 + i * 30, 10))
            i += 1
        if self.player.lifes - int(self.player.lifes) > 0:
            screen.blit(pygame.image.load("sprites/others/heart_1.png"), (200 + i * 30, 10))
            i += 1
        while i < MAX_LIFES:
            screen.blit(pygame.image.load("sprites/others/heart_0.png"), (200 + i * 30, 10))
            i += 1


if __name__ == "__main__":
    # size of the window
    size = width, height = 1080, 655
    speed = [1, 0]
    keys = []
    # background = pygame.image.load('sprites/scenes/scene_02.jpg').convert_alpha()
    screen = pygame.display.set_mode(size)

    background = Background('sprites/scenes/scene_02.jpg', [0, 0])
    player_morty = Player("morty",
                          Coord(100, 0, 0), [8, 0], 30, 10, 2, 2, 50)
    player_morty.lifes = 3.5
    myfont = pygame.font.SysFont("monospace bold", 40)
    # render text
    label = myfont.render("Level 1", 1, (0, 0, 0))
    level = Level(screen=screen, background=background, player=player_morty,
                  blocks=levels.LEVEL_1_BLOCKS + levels.LEVEL_1_FLOOR, objects=levels.LEVEL_1_OBJECTS, label=label)
    screen.fill([255, 255, 255])
    # screen.blit(background.image, background.rect)

    while 1:
        # Listen for quit keybord binding
        listen_for_exit()
        # Getting pressed keys
        keys = get_keys_clicked()
        # running level
        level.run(keys)
        # update display
        pygame.display.update()
        pygame.display.flip()