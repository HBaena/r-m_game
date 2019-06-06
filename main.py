import pygame
import subprocess
import sys
import threading
import levels
from Objects import Player, MAX_LIFES, MAX_ENERGY
from Miscellaneous import Coord
from sys import argv
from Objects import Block, Obtainable

BACKGROUND = [0, 0, 0]
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
        self.portal = None
        for obj in self.objects:
            if obj.name == 'portal':
                self.portal = obj
                break

    def run(self, keys):
        # if the energy is full open the portal

        if self.player.energy == MAX_ENERGY:
            if self.portal.portal_state == 'off':
                self.portal.open()

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
        # Erease player for refresh
        pygame.draw.rect(self.screen, BACKGROUND,
                         pygame.Rect(self.player.bounding.x - 50, self.player.bounding.y - 50,
                                     self.player.bounding.width + 80,
                                     self.player.bounding.height + 80), 0)

        # Refreshin objects
        for obj in self.objects:
            # if it is visible
            if obj.is_visible():
                # if is it a battery
                if obj.name == 'battery' or obj.name == 'portal':
                    # remove asset for new asset bigger or smaller
                    pygame.draw.rect(self.screen, BACKGROUND, (obj.bounding.x - 20, obj.bounding.y - 20,
                                                               obj.bounding.width + 30,
                                                               obj.bounding.height + 30), 0)
                    obj.refresh()
# refresh object
                self.screen.blit(obj.asset, obj.bounding)
            else:
                # if it is not visible hidde
                pygame.draw.rect(self.screen, BACKGROUND, obj.bounding, 0)
        # refresshing player and blocks
        RefreshScreen(self.screen, [self.player] + self.blocks)
        # Print label (lavel #)
        screen.blit(self.label, (10, 15))

        # Drawing hearts
        i = 0
        print("Lifes: ", self.player.lifes)
        while i < int(self.player.lifes):
            self.screen.blit(pygame.image.load("sprites/others/heart_2.png"), (200 + i * 30, 15))
            i += 1
        if self.player.lifes - int(self.player.lifes) > 0:
            self.screen.blit(pygame.image.load("sprites/others/heart_1.png"), (200 + i * 30, 15))
            i += 1
        while i < MAX_LIFES:
            self.screen.blit(pygame.image.load("sprites/others/heart_0.png"), (200 + i * 30, 15))
            i += 1

        # drawing power level
        self.screen.blit(pygame.image.load("sprites/others/portal_gun.png"), (600, 5))
        i = 0
        while i < self.player.energy:
            pygame.draw.rect(self.screen, (0, 255, 64), (680 + i * 15, 15, 10, 30), 0)
            i += 1
        while i < MAX_ENERGY:
            pygame.draw.rect(self.screen, (0, 255, 64), (680 + i * 15, 15, 10, 30), 1)
            i += 1


if __name__ == "__main__":
    # size of the window
    size = width, height = 1360, 760

    # size = width, height = 1480, 700
    speed = [1, 0]
    keys = []
    # background = pygame.image.load('sprites/scenes/scene_02.jpg').convert_alpha()
    screen = pygame.display.set_mode(size)
    # icon
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    background = Background('sprites/scenes/scene_02.jpg', [0, 0])
    if len(argv) == 1:
        name = 'morty'
    else:
        name = argv[1]
    if name == 'morty':
        player = levels.MORTY
    else:
        player = Player(name,
                        Coord(100, 0, 0), [8, 0], 30, 10, 2, 2, 50)

    player.energy = 8
    myfont = pygame.font.SysFont("monospace bold", 40)
    # render text
    label = myfont.render("Level 1", 1, (0, 0, 0))
    level = Level(screen=screen, background=background, player=player,
                  blocks=list(levels.LEVEL_1_BLOCKS + levels.LEVEL_1_FLOOR), objects=levels.LEVEL_1_OBJECTS,
                  label=label)
    screen.fill(BACKGROUND)
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
        # pygame.display.flip()
