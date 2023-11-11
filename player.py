from pico2d import (get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_DOWN, SDLK_UP,
                    SDLK_a, SDLK_1, SDLK_2, SDLK_3,
                    draw_rectangle)
import game_world
import game_framework

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
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
        # player.wait_time = get_time()

    @staticmethod
    def exit(player, e):
        # if a_down(e):
        #     player.action = 2
        #     player.frame = 0
        #     player.frame_wid = 130
        #     player.frame_hei = 215
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame  + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # if player.action == 2 and player.frame == 0:
        #     player.action = 0
        #     player.frame_wid = 102
        #     player.frame_hei = 162
        pass

    @staticmethod
    def draw(player):
        if player.idle_dir == 1:
            if player.role == 'knight':
                player.knight.clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                    100)
            elif player.role == 'magician':
                player.magician.clip_draw(int(player.frame) * 90, player.action * 162, 90, player.frame_hei, player.x, player.y, 66,
                                    100)
            elif player.role == 'viking':
                player.viking.clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                    100)
        else:
            if player.role == 'knight':
                player.knight.clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                    player.x, player.y, 66,
                                    100)
            elif player.role == 'magician':
                player.magician.clip_composite_draw(int(player.frame) * 90, player.action * 162, 90, player.frame_hei, 0, 'h',
                                    player.x, player.y, 66,
                                    100)
            elif player.role == 'viking':
                player.viking.clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                    player.x, player.y, 66,
                                    100)

class Walk:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.x_dir = 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.x_dir = -1
        elif up_down(e) or down_up(e):
            player.y_dir = 1
        elif down_down(e) or up_up(e):
            player.y_dir = -1
        player.action = 0

    @staticmethod
    def exit(player, e):
        # if a_down(e):
        #     player.action = 2
        #     player.frame = 0
        #     player.frame_wid = 130
        #     player.frame_hei = 215
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # if player.action == 2 and player.frame == 0:
        #     player.action = 0
        #     player.frame_wid = 102
        #     player.frame_hei = 162
        player.x += player.x_dir * 4
        player.y += player.y_dir * 3
        pass

    @staticmethod
    def draw(player):
        if player.x_dir == 1:
            if player.role == 'knight':
                player.knight.clip_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                    100)
            elif player.role == 'magician':
                player.magician.clip_draw(int(player.frame) * 90, player.action * 162, player.frame_wid, player.frame_hei, player.x, player.y, 66,
                                    100)
            elif player.role == 'viking':
                player.viking.clip_draw(int(player.frame) * player.frame_wid, player.action * 162, 90, player.frame_hei, player.x, player.y, 66,
                                    100)
        else:
            if player.role == 'knight':
                player.knight.clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                    player.x, player.y, 66,
                                    100)
            elif player.role == 'magician':
                player.magician.clip_composite_draw(int(player.frame) * 90, player.action * 162, 90, player.frame_hei, 0, 'h',
                                    player.x, player.y, 66,
                                    100)
            elif player.role == 'viking':
                player.viking.clip_composite_draw(int(player.frame) * player.frame_wid, player.action * 162, player.frame_wid, player.frame_hei, 0, 'h',
                                    player.x, player.y, 66,
                                    100)
        pass
    pass


class Sleep:
    pass



class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {a_down : Idle,  right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, up_up: Walk, up_down: Walk,down_up: Walk,down_down: Walk, time_out: Sleep},
            Walk: {a_down : Walk,  right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_up: Idle, up_down: Idle,down_up: Idle,down_down: Idle},
            Sleep: {right_down: Walk, left_down: Walk, right_up: Walk, left_up: Walk}}

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
        self.knight = load_image('resource/player/knight.png')
        self.magician = load_image('resource/player/magician.png')
        self.viking = load_image('resource/player/viking.png')
        self.state_machine = StateMachine(self)
        self.frame_wid = 102
        self.frame_hei = 162
        self.role = 'knight'
        self.roles = {down_1 : 'knight', down_2 : 'magician', down_3 : 'viking'}

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        for check_event, next_role in self.roles.items():
            if check_event(('INPUT',event)):
                self.role = next_role
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.x - 33, self.y - 50,self.x + 33, self.y + 50

    def handle_collision(self, group, other):
        if group == 'player:ball':
            pass
