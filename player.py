from pico2d import (get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_DOWN, SDLK_UP,
                    SDLK_a, SDLK_1, SDLK_2, SDLK_3,
                    draw_rectangle, clamp)
import game_world
import game_framework
from arrow import Arrow
from orb import Orb
from sword import Sword


# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def upkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def upkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def downkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def downkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def down_1(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_1

def down_2(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_2

def down_3(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_3

def time_out(e):
    return e[0] == 'TIME_OUT'


# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    @staticmethod
    def enter(player, e):
        player.idle_dir = player.x_dir
        player.x_dir = 0
        player.y_dir = 0
        player.frame = 0

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()


    @staticmethod
    def do(player):
        player.frame = (player.frame  + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162,
                                                player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                                100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162,
                                                          player.frame_wid, player.frame_hei, 0, 'h',
                                                          player.x, player.y, 66,
                                                          100)

class RunRight:
    @staticmethod
    def enter(player, e):
        player.x_dir = 1
        player.y_dir = 0
        pass

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                     100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                     player.x, player.y, 66,
                                     100)

class RunRightUp:
    @staticmethod
    def enter(player, e):
        player.x_dir = 1
        player.y_dir = 1
        pass

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)
        pass

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                     100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                     player.x, player.y, 66,
                                     100)

class RunRightDown:
    @staticmethod
    def enter(player, e):
        player.x_dir = 1
        player.y_dir = -1
        pass

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)
        pass

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                     100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                     player.x, player.y, 66,
                                     100)




class RunLeft:
    @staticmethod
    def enter(player, e):
        player.x_dir = -1
        player.y_dir = 0
        pass

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                     100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                     player.x, player.y, 66,
                                     100)


class RunLeftUp:
    @staticmethod
    def enter(player, e):
        player.x_dir = -1
        player.y_dir = 1
        pass

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                     100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                     player.x, player.y, 66,
                                     100)


class RunLeftDown:
    @staticmethod
    def enter(player, e):
        player.x_dir = -1
        player.y_dir = -1
        pass

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                     100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                     player.x, player.y, 66,
                                     100)




class RunUp:
    @staticmethod
    def enter(player, e):
        player.y_dir = 1


    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)
        pass

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                     100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                     player.x, player.y, 66,
                                     100)


class RunDown:
    @staticmethod
    def enter(player, e):
        player.y_dir = -1

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)
        pass

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            player.image[player.role].clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                     100)

        else:
            player.image[player.role].clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                     player.x, player.y, 66,
                                     100)


class Sleep:
    pass



class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft, upkey_down: RunUp,
                   downkey_down: RunDown, upkey_up: RunDown, downkey_up: RunUp, space_down: Idle},
            RunRight: {right_up: Idle, left_down: Idle, upkey_down: RunRightUp, upkey_up: RunRightDown,
                       downkey_down: RunRightDown, downkey_up: RunRightUp, space_down: RunRight},
            RunRightUp: {upkey_up: RunRight, right_up: RunUp, left_down: RunUp, downkey_down: RunRight,
                         space_down: RunRightUp},
            RunUp: {upkey_up: Idle, left_down: RunLeftUp, downkey_down: Idle, right_down: RunRightUp,
                    left_up: RunRightUp, right_up: RunLeftUp, space_down: RunUp},
            RunLeftUp: {right_down: RunUp, downkey_down: RunLeft, left_up: RunUp, upkey_up: RunLeft,
                        space_down: RunLeftUp},
            RunLeft: {left_up: Idle, upkey_down: RunLeftUp, right_down: Idle, downkey_down: RunLeftDown,
                      upkey_up: RunLeftDown, downkey_up: RunLeftUp, space_down: RunLeft},
            RunLeftDown: {left_up: RunDown, downkey_up: RunLeft, upkey_down: RunLeft, right_down: RunDown,
                          space_down: RunLeftDown},
            RunDown: {downkey_up: Idle, left_down: RunLeftDown, upkey_down: Idle, right_down: RunRightDown,
                      left_up: RunRightDown, right_up: RunLeftDown, space_down: RunDown},
            RunRightDown: {right_up: RunDown, downkey_up: RunRight, left_down: RunDown, upkey_down: RunRight,
                           space_down: RunRightDown}
        }

    def start(self):
        self.cur_state.enter(self.player)

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    def __init__(self):
        self.x, self.y = 300, 300
        self.frame = 0
        self.action = 0
        self.x_dir = 0
        self.y_dir = 0
        self.idle_dir = 0
        self.state_machine = StateMachine(self)
        self.frame_wid = 128
        self.frame_hei = 128
        self.role = 'knight'
        self.roles = {down_1 : 'knight', down_2 : 'magician', down_3 : 'viking'}
        self.stat = {'knight': {'power': 2, 'speed': 1.5, 'attack_speed': 0.9, 'weapon': Sword},
                     'wizard': {'power': 4, 'speed': 1, 'attack_speed': 0.7, 'weapon': Orb},
                     'archer': {'power': 6, 'speed': 1.2, 'attack_speed': 1.5, 'weapon': Arrow}}

        self.image = {'knight':load_image('resource/player/knight.png'),
                      'magician' : load_image('resource/player/magician.png'),
                      'viking':load_image('resource/player/viking.png')}
        self.frame_size = {'knight': (102, 162),
                      'magician': (90, 142),
                      'viking': (102,170) }


    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        for check_event, next_role in self.roles.items():
            if check_event(('INPUT',event)):
                self.role = next_role
                self.frame_wid, self.frame_hei = self.frame_size[self.role]
                print(self.frame_wid, self.frame_hei)
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def attack(self):
        weapon = self.stat[self.role]['weapon'](self.x + 40 * self.x_dir,self.y, self.stat[self.role]['power'], self.x_dir)
        game_world.add_object(weapon)

    def get_bb(self):
        return self.x - 33, self.y - 50,self.x + 33, self.y + 50

    def handle_collision(self, group, other):
        if group == 'player:ball':
            pass
