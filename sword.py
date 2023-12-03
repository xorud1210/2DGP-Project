from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import math

import server
import player

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Sword:
    def __init__(self, x, y, power, x_dir = 0, y_dir = 0):
        self.x = x
        self.y = y
        self.power = power
        self.x_dir = x_dir
        # if server.player.state_machine.before_stat:
        #     x_dir = 0.00000001
        # if server.player.state_machine.before_state== RunDown:
        #     x_dir = -0.00000001
        self.y_dir = y_dir
        self.speed = 0
        self.image = load_image('resource/vfx/sword1.png')
        self.frame = 0
        game_world.add_collision_pair('ball:sword',None,self)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if self.frame >= 2.8:
            game_world.remove_object(self)
        self.x += self.x_dir * RUN_SPEED_PPS * game_framework.frame_time * self.speed
        self.y += self.y_dir * RUN_SPEED_PPS * game_framework.frame_time * self.speed
        # player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        pass

    def draw(self):
        if self.x_dir == -1:
            self.image.clip_draw(int(self.frame) * 114, 0,114,217,self.x,self.y,60,120)
        else:
            self.image.clip_composite_draw(int(self.frame) * 114, 0,114,217,0,'h',self.x,self.y,60,120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20., self.y - 60, self.x + 20, self.y + 60

    def handle_collision(self, group, other):
        if group == 'ball:sword':
            other.dir = math.atan2(other.y - self.y, other.x - self.x)
            other.x_dir = math.cos(other.dir) * self.power
            other.y_dir = math.sin(other.dir) * self.power
        pass