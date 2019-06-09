import pygame
import subprocess
import sys
import time
import threading
from levels import LEVELS
from Objects import Player, MAX_LIFES, MAX_ENERGY
from Miscellaneous import Coord
from sys import argv
from Objects import Block, Obtainable
size = width, height = 1360, 760
BACKGROUND = [0, 0, 0]
BLOCK_SIZE = 30
PLAYER_SCALE = 0.5
K_SPACE = 6
K_ENTER = 7
LEVEL_REBOOT = 2
LEVEL_PASSED = 1
LEVEL_RUNNING = 0

USED_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT,
             pygame.K_LEFT, pygame.K_RSHIFT, pygame.K_LSHIFT,
             pygame.K_SPACE, pygame.K_RETURN]


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
        self.portal = None
        for obj in self.objects:
            if obj.name == 'portal':
                self.portal = obj
                break
        self.portal.portal_state = 'off'
        # myfont = pygame.font.SysFont("roboto bold", 100)
        # render text
        self.tmp_01 = 0
        self.tmp_02 = 0

    def run(self, keys):
        # if the portal is closing it changes to next level
        if self.portal.portal_state is 'close':
            if keys[K_ENTER] == 1:
                return LEVEL_PASSED

            if self.tmp_01 == 0:
                image = pygame.image.load('sprites/labels/next_level.png')
                x = int(image.get_rect()[2])
                y = int(image.get_rect()[3])
                self.screen.blit(image, (int(width/2 - x/2), int(height/2 - y/2 - 100)))
                self.tmp_01 = 1

            return LEVEL_RUNNING

        # if the energy is full open the portal
        if self.player.energy == MAX_ENERGY:
            if self.portal.portal_state == 'off':
                self.portal.open()

        # if player is death reboot level
        
        if not player.is_alive():
            if self.tmp_02 == 0:
                image = pygame.image.load('sprites/labels/death.png')
                x = int(image.get_rect()[2])
                y = int(image.get_rect()[3])
                self.screen.blit(image, (int(width/2 - x/2), int(height/2 - y/2 - 100)))
                self.tmp_02 = 1

            if keys[K_ENTER] == 1:
                del self.objects
                del self.blocks
                return LEVEL_REBOOT

            return LEVEL_RUNNING

        self.change_movement(keys)
        self.refresh_screen()
        return LEVEL_RUNNING

    def change_movement(self, keys):
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
                if obj.name == 'battery':
                    # remove asset for new asset bigger or smaller
                    pygame.draw.rect(self.screen, BACKGROUND, (obj.bounding.x - 20, obj.bounding.y - 20,
                                                               obj.bounding.width + 30,
                                                               obj.bounding.height + 30), 0)
                    obj.refresh()
                elif obj.name is 'portal':
                    pygame.draw.rect(self.screen, BACKGROUND, (obj.bounding.x - 50, obj.bounding.y - 50,
                                                               obj.bounding.width + 50,
                                                               obj.bounding.height + 50), 0)
                    obj.refresh()
                elif obj.name is 'canon':
                    pygame.draw.rect(self.screen, BACKGROUND, (obj.bounding.x - 20, obj.bounding.y - 20,
                                                               obj.bounding.width + 30,
                                                               obj.bounding.height + 30), 0)
                    obj.shoot()
                    for bullet in obj.shoots:
                        bullet.refresh(screen, BACKGROUND)
                        if self.player.bounding.colliderect(bullet.bounding):
                            self.player.get_obtainable(bullet)

                            pygame.draw.rect(self.screen, BACKGROUND, (bullet.bounding.x - 20, bullet.bounding.y - 20,
                                                                       bullet.bounding.width + 30,
                                                                       bullet.bounding.height + 30), 0)
                            del obj.shoots[obj.shoots.index(bullet)]


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
    ''' PYGAME '''
    speed = [1, 0]
    keys = []
    # background = pygame.image.load('sprites/scenes/scene_02.jpg').convert_alpha()
    screen = pygame.display.set_mode(size)
    # icon
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    background = Background('sprites/scenes/scene_02.jpg', [0, 0])
    ''' PYGAME '''

    ''' PLAYER '''
    if len(argv) == 1:
        name = 'morty'
    else:
        name = argv[1]
    if name == 'morty':
        player = Player('morty', Coord(100, 0, 0), [8, 0], 50, 10, 2, 2, 50)
    else:
        player = Player(name,
                        Coord(100, 0, 0), [8, 0], 50, 10, 2, 2, 50)
    player.energy = 8
    player.lifes = MAX_LIFES
    ''' PLAYER '''

    ''' LABAEL '''
    myfont = pygame.font.SysFont("monospace bold", 40)
    # render text
    label = myfont.render("Level 1", 1, (0, 0, 0))
    ''' LABAEL '''

    ''' RUNING LEVELS'''
    i = 0
    while i < len(LEVELS):
        player = Player(name,
                        Coord(100, 0, 0), [8, 0], 50, 10, 2, 2, 50)
        player.lifes = MAX_LIFES
        player.energy = 0
        player.mx_jump = 15
        level = Level(screen=screen, background=background, player=player,
                      blocks=LEVELS[i][0].copy(), objects=LEVELS[i][1].copy(),
                      label=label)
        screen.fill(BACKGROUND)

        # screen.blit(background.image, background.rect)
        while 1:
            # Listen for quit keybord binding
            listen_for_exit()
            # Getting pressed keys
            keys = get_keys_clicked()
            # running level
            response = level.run(keys)
            if response == LEVEL_PASSED:
                break
            elif response == LEVEL_REBOOT:
                # Restart level
                for obj in LEVELS[i][1]:
                    obj.visible = True
                i -= 1
                break
            
            # update display
            pygame.display.update()
            # pygame.display.flip()
        i += 1

    ''' RUNING LEVELS'''


    

    ''' EXIT LABEL '''
    screen.fill(BACKGROUND)
    image = pygame.image.load('sprites/labels/end_game.png')
    x = int(image.get_rect()[2])
    y = int(image.get_rect()[3])
    screen.blit(image, (int(width/2 - x/2), int(height/2 - y/2 - 100)))
    pygame.display.update()
    ''' EXIT LABEL '''

    ''' END GAME '''
    while 1:
        listen_for_exit()

    ''' END GAME '''
