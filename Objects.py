import pygame

K_UP = 0
K_DOWN = 1
K_RIGHT = 2
K_LEFT = 3
K_RSHIFT = 4
K_LSHIFT = 5
K_SPACE = 6

DELAY_X = 7
DELAY_Y = 10
BLOCK_SIZE = 30
PLAYER_SCALE = 0.5
GRAVITY = 2
JUMP_STAY = 10
MAX_LIFES = 10
MAX_ENERGY = 10
BOTTOM_TOLERANCE = 4


class Collisions():
    """docstring for Collisions"""

    def __init__(self):
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False
        self.rect_top = None
        self.rect_bottom = None
        self.rect_left = None
        self.rect_right = None


class Object():
    """docstring for Object"""

    def __init__(self, asset, position):
        print('Init: Object')
        self.asset = None
        self.set_asset(asset)
        self.position = position
        self.name = ''
        self.bounding = self.asset.get_rect()
        self.bounding.x, self.bounding.y = position.x, position.y
        self.collisions = Collisions()
        self.visible = True

    def is_visible(self):
        return self.visible

    def set_name(self, name):
        self.name = name

    def set_asset(self, rute):
        if self.__str__ == 'block':
            self.asset = pygame.image.load(rute).convert()
        else:
            self.asset = pygame.image.load(rute)

        self.asset = pygame.transform.scale(
            self.asset, (int(self.asset.get_rect()[2] * PLAYER_SCALE),
                         int(self.asset.get_rect()[3] * PLAYER_SCALE)))

    def show(self):
        print("show")

    def hide(self):
        print("hide")

    def destroy(self):
        print("destroy")

    def is_colliding(self, obj):
        print("is_colliding")


class Saw(Object):
    def __init__(self, position):
        asset_name = 'sprites/others/saw_1.png'
        Object.__init__(self, asset_name, position)
        self.name = 'saw'
        self.state = 1
        self.count = 0
        self.delay = 20

    def rotate(self):
        if not self.count % self.delay:
            print("Rotate: ", self.state)
            asset = 'sprites/others/saw_' + str(self.state) + '.png'
            self.asset = pygame.image.load(asset)
            if self.state == 4:
                self.state = 0
            self.state += 1

        self.count += 1


class Obtainable(Object):
    """docstring for Obtainable"""

    def __init__(self, position, asset, name=''):
        Object.__init__(self, asset, position)
        self.__str__ = 'obtainable'
        self.name = name

    def active_action(self, player):
        player.obtainable_action(self.name)


class Portal(Obtainable):

    def __init__(self, position):
        asset = 'sprites/portal/portal_open/portal_open_1.png'
        Obtainable.__init__(self, position, asset)
        self.name = 'portal'
        self.state = 1
        self.portal_state = 'open'
        self.count = 1
        self.delay = 10

    def refresh(self):
        if not self.count % self.delay:
            if self.portal_state == 'open':
                self.set_asset('sprites/portal/portal_open/portal_open_' + str(int(self.count / self.delay)) + '.png')
                if self.state != 32:
                    self.state += 1
                else:
                    self.portal_state = 'running'
                    self.state = 1
                    self.count = 1

            elif self.portal_state == 'running':
                self.set_asset('sprites/portal/portal_running/portal_' + str(int(self.count / self.delay)) + '.png')
                if self.state != 31:
                    self.state += 1
                else:
                    self.count = 1
                    self.state = 2
            elif self.portal_state == 'close':
                self.set_asset('sprites/portal/portal_close/portal_close_' + str(int(self.count / self.delay)) + '.png')
                if self.state != 32:
                    self.state += 1
                else:
                    self.count = 1
                    self.state = 1
                    self.visible = False
                    self.portal_state = 'closed'

        self.count += 1


class Battery(Obtainable):
    def __init__(self, position, asset, charge):
        self.charge = charge
        Obtainable.__init__(self, position, asset, 'battery')
        self.state = 1
        self.delay = 70


class SuperBattery(Object):

    def __init__(self, position):
        asset = 'sprites/others/battery_super_1.png'
        Battery.__init__(self, position, asset, 2)

    def refresh(self):
        if self.state == 0:
            self.set_asset('sprites/others/battery_super_1.png')
        elif self.state == self.delay:
            self.set_asset('sprites/others/battery_super_2.png')

        self.state += 1
        if self.state == self.delay * 2:
            self.state = 0


class NormalBattery(Battery):

    def __init__(self, position):
        asset = 'sprites/others/battery_normal_1.png'
        Battery.__init__(self, position, asset, 1)

    def refresh(self):
        if self.state == 0:
            self.set_asset('sprites/others/battery_normal_1.png')
        elif self.state == self.delay:
            self.set_asset('sprites/others/battery_normal_2.png')

        self.state += 1
        if self.state == self.delay * 2:
            self.state = 0


class Block(Object):
    """docstring for Block"""

    def __init__(self, position, asset):
        print("Init: block")
        self.asset_name = 'sprites/block/' + asset + '.png'
        super(Block, self).__init__(self.asset_name, position)
        self.asset = pygame.transform.scale(
            self.asset, (BLOCK_SIZE, BLOCK_SIZE))
        self.__str__ = 'block'
        # Spikes
        self.edge = None


class Sprike(Object):
    """docstring for Sprike"""

    def __init__(self, position, asset):
        print("Init: Sprike")
        self.asset_name = 'sprites/block/' + asset + '.png'
        super(Sprike, self).__init__(self.asset_name, position)
        self.asset = pygame.transform.scale(
            self.asset, (BLOCK_SIZE, BLOCK_SIZE))
        self.__str__ = 'sprike'
        # Spikes


class Character(Object):
    """docstring for Character"""

    def __init__(self, asset, position, speed):
        self.asset_name = 'sprites/' + asset + '/' + asset
        super(Character, self).__init__(
            self.asset_name + '_stop.png', position)
        print('Init: Character')
        # number of lifes
        self.lifes = MAX_LIFES
        # speed[0] horizontal (constant)
        # speed[0] vertical (variable)
        self.speed = speed
        # walking direction
        self.direction = 'r'
        # standing on a block edge
        self.edge = True
        # sprit walk state
        self.walk_state = 0
        # delay to do movement
        self.count_delay_x = DELAY_X
        self.count_delay_y = DELAY_Y

    def is_alive(self):
        if self.lifes < 0:
            print('Dead')
            return False
        else:
            print('Alive')
            return True

    def walk(self, direction, left_edge, right_edge, rects):
        if self.count_delay_x < DELAY_X:
            self.count_delay_x += 1
            return
        self.count_delay_x = 0

        if direction is 'r':
            if self.bounding.right < right_edge:
                if self.collisions.right is False:
                    self.bounding = self.bounding.move(self.speed[0], 0)
                    self.detect__horizontal_collisions(rects, direction, left_edge,
                                                       right_edge)
                    if self.collisions.right is True:
                        self.bounding = self.bounding.move(
                            -(self.bounding.right - self.collisions.rect_right.bounding.left), 0)

        else:
            if self.bounding.left > left_edge:
                if self.collisions.left is False:
                    self.bounding = self.bounding.move(-self.speed[0], 0)
                    self.detect__horizontal_collisions(rects, direction, left_edge,
                                                       right_edge)
                    if self.collisions.left is True:
                        self.bounding = self.bounding.move(
                            -(self.bounding.left - self.collisions.rect_left.bounding.right) + 6, 0)

        if self.walk_state == 0 or self.walk_state == 4:
            self.walk_state = 1
        else:
            self.walk_state += 1

        '''
        '''
        if self.state_y in [1, 2]:
            self.set_asset(self.asset_name + '_walk_' + direction +
                           '_' + str(2) + '.png')
        else:
            self.set_asset(self.asset_name + '_walk_' + direction +
                           '_' + str(self.walk_state) + '.png')

    def run(self, direction, left_edge, right_edge, rects):
        if self.count_delay_x < DELAY_X:
            self.count_delay_x += 1
            return
        self.count_delay_x = 0

        if direction is 'r':
            if self.bounding.right < right_edge:
                if self.collisions.right is False:
                    self.bounding = self.bounding.move(self.speed[0] + int((self.speed[0] * self.run_percent) / 100), 0)
                    self.detect__horizontal_collisions(rects, direction, left_edge,
                                                       right_edge)
                    if self.collisions.right is True:
                        self.bounding = self.bounding.move(
                            -(self.bounding.right - self.collisions.rect_right.bounding.left), 0)

        else:
            if self.bounding.left > left_edge:
                if self.collisions.left is False:
                    self.bounding = self.bounding.move(-(self.speed[0] + int((self.speed[0] * self.run_percent) / 100)),
                                                       0)
                    self.detect__horizontal_collisions(rects, direction, left_edge,
                                                       right_edge)
                    if self.collisions.left is True:
                        self.bounding = self.bounding.move(
                            -(self.bounding.left - self.collisions.rect_left.bounding.right) + 6, 0)

        if self.walk_state == 0 or self.walk_state == 4:
            self.walk_state = 1
        else:
            self.walk_state += 1
        '''
        '''
        if self.state_y in [1, 2]:
            self.set_asset(self.asset_name + '_walk_' + direction +
                           '_' + str(2) + '.png')
        else:
            self.set_asset(self.asset_name + '_walk_' + direction +
                           '_' + str(self.walk_state) + '.png')

    def stop(self):
        self.walk_state = 0
        self.set_asset(self.asset_name + '_stop.png')
        # self.bounding = self.bounding.move(0, self.speed[1])


class Player(Character):
    """docstring for Player"""

    def __init__(self, asset, position, speed, jump, jump_stay, weight, resistence, run):
        Character.__init__(self, asset, position, speed)
        self.__str__ = 'player'
        print('Init: Player')
        # Point
        self.points = 0
        # key
        self.key = False
        # count from stop to max_jump (or before)
        self.count_jump = 0
        # max jumpping
        self.max_jump = jump
        # states staying on top of jump
        self.jump_stay = jump_stay
        # resistence to attacks
        self.weight = weight
        self.resistence = resistence
        # Percent increased while running
        self.run_percent = run
        # states of movement
        self.state_x = 0
        self.state_y = 0
        # temp variables
        self.__key_jump = 0
        self.energy = 0

    def attacked(self, enemy):
        print('Attacked')
        self.lifes -= enemy.power

    def get_obtainable(self, obtainable):
        if obtainable.name is 'life':
            print('Incrementing lifes')
            self.lifes += 1
            if self.lifes > MAX_LIFES:
                self.lifes = MAX_LIFES
        elif obtainable.name is 'portal':
            if obtainable.portal_state is not 'off':
                return
            if obtainable.portal_state is not 'close':
                obtainable.state = 1
                obtainable.count = 1
                obtainable.portal_state = 'close'

        elif obtainable.name is 'spike':
            print("Spike")
            self.lifes -= 1
            self.is_alive()
            obtainable.visible = False
        elif obtainable.name is 'battery':
            self.energy += obtainable.charge
            obtainable.visible = False

    def is_colliding(self, obj):
        print("is_colliding: Player")
        if obj.__str__ is 'obtainable':
            self.get_obtainable(obj)
        elif obj.__str__ is 'enemy':
            self.attacked(obj)

    def __bottom_collision(self, rect):

        # Collision normal
        if self.bounding.bottom - rect.bounding.top == 1:
            # print("bottom", self.bounding.bottom - rect.bounding.top)
            return True
        elif (
                self.bounding.bottom - rect.bounding.top > 1 and
                self.bounding.bottom - rect.bounding.top < 5
        ):
            self.bounding.move(0, (rect.bounding.top - self.bounding.bottom + 10))
            return True
        else:
            return False

    def __top_collision(self, rect):
        if self.bounding.bottom - rect.bounding.top == -1:
            return True
        elif rect.bounding.bottom - self.bounding.top > 1:
            self.bounding.move(0, (self.bounding.bottom - rect.bounding.top) + 1)
            return True
        else:
            return False

    def __left_collision(self, rect, direction):
        if (
                self.bounding.left < rect.bounding.right and
                self.bounding.left > rect.bounding.left and
                direction == 'l'
        ):
            return True
        else:
            return False

    def __right_collision(self, rect, direction):
        if (
                self.bounding.right > rect.bounding.left and
                self.bounding.right < rect.bounding.right and
                direction == 'r'
        ):
            return True
        else:
            return False

    def _objects_collisions(self, objects):
        collisions = []
        for obj in objects:
            if self.bounding.colliderect(obj.bounding):
                collisions.append(obj)

        return collisions

    def detect__vertical_collisions(self, rects):
        self.collisions.bottom = False
        self.collisions.top = False
        self.collisions.rect_bottom = None
        self.collisions.rect_top = None

        for rect in rects:
            if self.bounding.colliderect(rect.bounding):
                if (self.__bottom_collision(rect)):
                    self.collisions.bottom = True
                elif (self.__top_collision(rect)):
                    self.collisions.top = True

    def detect__horizontal_collisions(self, rects, direction, left_edge,
                                      right_edge):
        self.collisions.right = False
        self.collisions.left = False
        self.collisions.rect_right = None
        self.collisions.rect_left = None

        for rect in rects:
            if self.bounding.colliderect(rect.bounding):
                if self.__bottom_collision(rect):
                    continue
                if self.__right_collision(rect, direction):
                    self.collisions.right = True
                    self.collisions.rect_right = rect
                    # print(self.bounding.right - rect.bounding.left)
                    return [left_edge, rect.bounding.left]
                elif self.__left_collision(rect, direction):
                    # print(self.bounding.left - rect.bounding.right)
                    self.collisions.left = True
                    self.collisions.rect_left = rect
                    print("Left collision")
                    return [rect.bounding.right, right_edge]

        return None

    def change_movement_y(self, jump, rects, none1, none2):
        # State 1 (Falling)
        if (
                (
                        (self.state_y == 0 or self.state_y == 1) and
                        self.collisions.bottom is False
                ) or
                (
                        self.state_y == 2 and
                        self.count_jump >= self.max_jump
                ) or
                (
                        self.state_y == 2 and
                        jump == 0
                )
                or
                (
                        self.state_y == 2 and
                        self.collisions.top is True
                )
        ):
            self.speed[1] = GRAVITY * self.weight
            self.state_y = 1
            self.count_jump = 0
        # State 2 (rising)
        elif (
                (
                        self.state_y == 0 and
                        jump == 1 and
                        self.count_jump == 0 and
                        self.collisions.bottom is True and
                        self.collisions.top is False and
                        self.__key_jump != jump
                ) or
                (
                        self.state_y == 2 and
                        jump == 1 and
                        self.count_jump != self.max_jump and
                        self.collisions.top is False
                )

        ):
            # Last pixels it keps "flying" 
            if self.count_jump >= self.max_jump - int(self.jump_stay / 2):
                self.speed[1] = 0
            # Before last pixels it just rises less
            elif self.count_jump >= self.max_jump - self.jump_stay:
                self.speed[1] = -1 * GRAVITY
            else:
                # Normaly rising
                self.speed[1] = -2 * GRAVITY

            self.count_jump += 1
            self.state_y = 2

        # State 0 (stopped)
        elif (
                (
                        self.state_y == 0 and
                        jump == 0 and
                        self.collisions.bottom is True) or
                (
                        self.state_y == 0 and
                        self.collisions.top is True and
                        self.collisions.bottom is True
                ) or
                (
                        self.collisions.bottom is True
                )

        ):
            # Stay without fall neither raise
            self.speed[1] = 0
            self.state_y = 0
            self.count_jump = 0
        # Store the last key_jump state (pressed or not pressed)
        self.__key_jump = jump
        self.bounding = self.bounding.move(0, self.speed[1])
        self.detect__vertical_collisions(rects)

    def change_movement_x(self, keys, left_edge, right_edge, rects, objects):

        objs = self._objects_collisions(objects)
        if objs != []:
            for obj in objs:
                # obj = Obtainable([], "s", "")
                print("Is", obj.name)
                if obj.is_visible():
                    self.get_obtainable(obj)

        # state 0 (stopped) (first state)
        if (
                (
                        # From stop to stop
                        self.state_x == 0 and
                        keys[K_RIGHT] == 0 and
                        keys[K_LEFT] == 0
                ) or
                (
                        # From wherever to stop
                        # Doesn't need ask for state or shifts
                        keys[K_RIGHT] == 0 and
                        keys[K_LEFT] == 0
                )
        ):

            self.count_delay_x = DELAY_X
            self.state_x = 0
            self.stop()
            if self.speed[1] != 0:
                self = self.bounding.move(0, self.speed[1])
            return
        # State 1 (walk to right)
        elif (
                (
                        # From stop to walk-right or walk-left to walk-right
                        (self.state_x == 0 or self.state_x == 2) and
                        keys[K_LEFT] == 0 and
                        keys[K_RIGHT] == 1 and
                        (keys[K_RSHIFT] == 0 and keys[K_LSHIFT] == 0)
                ) or
                (
                        # From walk-right to walk-right or run-right to walk-right
                        (self.state_x == 1 or self.state_x == 3) and
                        keys[K_RIGHT] == 1 and
                        (keys[K_RSHIFT] == 0 and keys[K_LSHIFT] == 0)
                )
        ):
            if self.state_x == 2:
                self.count_delay_x = DELAY_X
            self.state_x = 1
            edges = self.detect__horizontal_collisions(
                rects, 'r', left_edge, right_edge)

            if edges is not None:
                left_edge, right_edge = edges[0], edges[1]
            self.walk('r', left_edge, right_edge, rects)
            return

        # State 2 (walk to left)
        elif (
                (
                        # From stop to walk-right or walk-left to walk-right
                        (self.state_x == 0 or self.state_x == 1) and
                        keys[K_LEFT] == 1 and
                        keys[K_RIGHT] == 0 and
                        (keys[K_RSHIFT] == 0 and keys[K_LSHIFT] == 0)
                ) or
                (
                        # From walk-left to walk-left or run-left to walk-left
                        (self.state_x == 2 or self.state_x == 4) and
                        keys[K_LEFT] == 1 and
                        (keys[K_RSHIFT] == 0 and keys[K_LSHIFT] == 0)
                )
        ):
            if self.state_x == 1:
                self.count_delay_x = DELAY_X
            self.state_x = 2
            edges = self.detect__horizontal_collisions(
                rects, 'l', left_edge, right_edge)
            if self.collisions.rect_left is not None:
                print(self.collisions.rect_left)
                input()
            if edges is not None:
                left_edge, right_edge = edges[0], edges[1]
            self.walk('l', left_edge, right_edge, rects)
            return
        # State 3 (run to right)
        elif (
                (
                        # From stop to run-right
                        (self.state_x == 0 or self.state_x == 4) and
                        keys[K_LEFT] == 0 and
                        keys[K_RIGHT] == 1 and
                        (keys[K_RSHIFT] == 1 or keys[K_LSHIFT] == 1)
                ) or
                (
                        # From run-right to run-right or walk-right to run-right
                        (self.state_x == 1 or self.state_x == 3) and
                        keys[K_RIGHT] == 1 and
                        (keys[K_RSHIFT] == 1 or keys[K_LSHIFT] == 1)
                )
        ):
            self.state_x = 3
            edges = self.detect__horizontal_collisions(
                rects, 'r', left_edge, right_edge)
            if edges is not None:
                left_edge, right_edge = edges[0], edges[1]
            self.run('r', left_edge, right_edge, rects)
            return

        # State 4 (run to left)
        elif (
                (
                        # From stop to walk-right or walk-left to walk-right
                        (self.state_x == 0 or self.state_x == 3) and
                        keys[K_LEFT] == 1 and
                        keys[K_RIGHT] == 0 and
                        (keys[K_RSHIFT] == 1 or keys[K_LSHIFT] == 1)
                ) or
                (
                        # From walk-left to walk-left or run-left to walk-left
                        (self.state_x == 2 or self.state_x == 4) and
                        keys[K_LEFT] == 1 and
                        (keys[K_RSHIFT] == 1 or keys[K_LSHIFT] == 1)
                )
        ):
            self.state_x = 4
            edges = self.detect__horizontal_collisions(
                rects, 'l', left_edge, right_edge)
            if edges is not None:
                left_edge, right_edge = edges[0], edges[1]
            self.run('l', left_edge, right_edge, rects)
            return

        print(self.state_x, keys[K_LEFT], keys[K_RIGHT],
              keys[K_LSHIFT], keys[K_SPACE])
        input()


class Enemy(Character):
    """docstring for Enemy"""
    counter = 0

    def __init__(self, asset, position, speed, power):
        Character.__init__(self, asset, position, speed)
        self.__str__ = 'enemy'
        print('Init: Enemy')
        self.power = power
        Enemy.counter += 1

    def __del__(self):
        Enemy.counter -= 1
        pass

    def attack(self, player):
        player.lifes -= self.power

    def change_direction(self, block):
        if block.edge:
            self.direction = 'l' if self.direction is 'r' else 'r'
