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

def attack_end(e):
    return e[0] == 'ATTACK_END'

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
        # player.x_dir = 0
        player.y_dir = 0
        player.frame = 0
        player.action = 9
        player.max_frame = player.sprite[player.role]['max_frame']['idle']

    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def do(player):
        player.frame = (player.frame  + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

class RunRight:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if player.run and player.x_dir == 1:
            player.action = 7
        else:
            player.run = False
            player.action = 8
            if right_up(e):
                player.input_time = get_time()
            if right_down(e):
                if get_time() - player.input_time < game_framework.frame_time * 60:
                    player.action = 7
                    player.run = True
                else:
                    player.action = 8
                    player.run = False
            player.input_time = get_time()
        player.x_dir = 1
        player.y_dir = 0
        if player.action == 7:
            player.max_frame = player.sprite[player.role]['max_frame']['run']
        elif player.action == 8:
            player.max_frame = player.sprite[player.role]['max_frame']['walk']
        pass

    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)


class RunRightUp:
    @staticmethod
    def enter(player, e):
        player.x_dir = 1
        player.y_dir = 1
        player.state_change('walk')

    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)
        pass


class RunRightDown:
    @staticmethod
    def enter(player, e):
        player.x_dir = 1
        player.y_dir = -1
        player.state_change('walk')
    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)
        pass

class RunLeft:
    @staticmethod
    def enter(player, e):
        player.x_dir = -1
        player.y_dir = 0
        player.state_change('walk')

    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)



class RunLeftUp:
    @staticmethod
    def enter(player, e):
        player.x_dir = -1
        player.y_dir = 1
        player.state_change('walk')

    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)

class RunLeftDown:
    @staticmethod
    def enter(player, e):
        player.x_dir = -1
        player.y_dir = -1
        player.state_change('walk')

    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)





class RunUp:
    @staticmethod
    def enter(player, e):
        player.y_dir = 1
        player.state_change('walk')


    @staticmethod
    def exit(player, e):
        pass


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)
        pass


class RunDown:
    @staticmethod
    def enter(player, e):
        player.y_dir = -1
        player.state_change('walk')

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # player.x += player.x_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        player.x = clamp(25, player.x, 1600 - 25)     # clamp : 값의 범위 지정
        player.y = clamp(25, player.y, 900 - 25)

class Attack:
    @staticmethod
    def enter(player, e):
        player.run = False
        player.frame = 0
        player.state_change('atk1')

    @staticmethod
    def exit(player, e):
        if player.frame >= player.max_frame-0.1:
            if player.state_machine.cur_state == RunUp or player.state_machine.cur_state == RunDown:
                player.attack(0, player.y_dir)
            else:
                player.attack(player.x_dir,player.y_dir)

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * player.attack_speed * game_framework.frame_time ) % player.max_frame
        if player.frame >= player.max_frame-0.2:
            player.state_machine.handle_event(('ATTACK_END', 0))


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft, upkey_down: RunUp, downkey_down: RunDown, upkey_up: RunDown, downkey_up: RunUp, space_down: Attack},
            RunRight: {right_up: Idle, left_down: Idle, upkey_down: RunRightUp, upkey_up: RunRightDown,
                       downkey_down: RunRightDown, downkey_up: RunRightUp, space_down: Attack},
            RunRightUp: {upkey_up: RunRight, right_up: RunUp, left_down: RunUp, downkey_down: RunRight,
                         space_down: Attack},
            RunUp: {upkey_up: Idle, left_down: RunLeftUp, downkey_down: Idle, right_down: RunRightUp,
                    left_up: RunRightUp, right_up: RunLeftUp, space_down: Attack},
            RunLeftUp: {right_down: RunUp, downkey_down: RunLeft, left_up: RunUp, upkey_up: RunLeft,
                        space_down: Attack},
            RunLeft: {left_up: Idle, upkey_down: RunLeftUp, right_down: Idle, downkey_down: RunLeftDown,
                      upkey_up: RunLeftDown, downkey_up: RunLeftUp, space_down: Attack},
            RunLeftDown: {left_up: RunDown, downkey_up: RunLeft, upkey_down: RunLeft, right_down: RunDown,
                          space_down: Attack},
            RunDown: {downkey_up: Idle, left_down: RunLeftDown, upkey_down: Idle, right_down: RunRightDown,
                      left_up: RunRightDown, right_up: RunLeftDown, space_down: Attack},
            RunRightDown: {right_up: RunDown, downkey_up: RunRight, left_down: RunDown, upkey_down: RunRight, space_down: Attack},
            Attack:{right_down: RunRight, left_down: RunLeft, upkey_down: RunUp,
                   downkey_down: RunDown, attack_end: Idle}
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
        self.x_dir = 0
        self.y_dir = 0
        self.run = False
        self.input_time = 0
        self.idle_dir = 0
        self.state_machine = StateMachine(self)

        self.frame_wid = 128
        self.frame_hei = 128
        self.max_frame = 6
        self.frame = 0
        self.action = 9

        self.speed = 1.5
        self.attack_speed = 0.6
        self.role = 'knight'
        self.roles = {down_1 : 'knight', down_2 : 'wizard', down_3 : 'archer'}
        self.stat = {'knight': {'power': 2, 'speed': 1.5, 'attack_speed': 0.9, 'weapon': Sword},
                     'wizard': {'power': 4, 'speed': 1, 'attack_speed': 0.7, 'weapon': Orb},
                     'archer': {'power': 6, 'speed': 1.2, 'attack_speed': 1.5, 'weapon': Arrow}}
        self.image = {'knight':load_image('resource/player/knight.png'),
                      'wizard' : load_image('resource/player/wizard.png'),
                      'archer':load_image('resource/player/archer.png')}
        self.sprite = {
            'knight': {'max_frame': {'idle': 6, 'walk': 8, 'run': 7, 'atk1': 5, 'atk2': 2, 'atk3': 3, 'atk4': 4},
                       'action': {'idle': 9, 'walk': 8, 'run': 7, 'atk1': 6, 'atk2': 5, 'atk3': 4, 'atk4': 3}},
            'wizard': {'max_frame': {'idle': 6, 'walk': 7, 'run': 8, 'atk1': 10, 'atk2': 4, 'atk3': 7},
                       'action': {'idle': 9, 'walk': 8, 'run': 7, 'atk1': 5, 'atk2': 4, 'atk3': 3}},
            'archer': {'max_frame': {'idle': 6, 'walk': 8, 'run': 8, 'atk1': 14, 'atk2': 13, 'atk3': 4},
                       'action': {'idle': 9, 'walk': 8, 'run': 7, 'atk1': 5, 'atk2': 4, 'atk3': 3}},
        }


    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        for check_event, next_role in self.roles.items():
            if check_event(('INPUT',event)):
                self.role = next_role
                self.speed, self.attack_speed = self.stat[self.role]['speed'], self.stat[self.role]['attack_speed']

    def draw(self):
        if self.x_dir == 1:
            self.image[self.role].clip_draw(int(self.frame) * self.frame_wid, self.action * self.frame_hei,
                                            self.frame_wid, self.frame_hei, self.x, self.y + 25,
                                            self.frame_wid, self.frame_hei)

        else:
            self.image[self.role].clip_composite_draw(int(self.frame) * self.frame_wid,
                                                      self.action * self.frame_hei, self.frame_wid,
                                                      self.frame_hei, 0, 'h', self.x, self.y + 25,
                                                      self.frame_wid, self.frame_hei)

    def state_change(self, state):
        self.action = self.sprite[self.role]['action'][state]
        self.max_frame = self.sprite[self.role]['max_frame'][state]

    def attack(self):
        weapon = self.stat[self.role]['weapon'](self.x + 40 * self.x_dir,self.y, self.stat[self.role]['power'], self.x_dir)
        game_world.add_object(weapon)

    def get_bb(self):
        return self.x - 33, self.y - 50,self.x + 33, self.y + 50

    def handle_collision(self, group, other):
        if group == 'player:ball':
            pass
