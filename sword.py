from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import math

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
    def __init__(self, x, y, power, dir = 0):
        self.x = x
        self.y = y
        self.power = power
        self.dir = dir
        self.speed = 0
        self.image = load_image('resource/vfx/sword1.png')
        self.frame = 0
        game_world.add_collision_pair('ball:sword',None,self)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if self.frame >= 2.9:
            game_world.remove_object(self)
        self.x += self.dir  * RUN_SPEED_PPS * game_framework.frame_time * self.speed
        # player.y += player.y_dir * RUN_SPEED_PPS * game_framework.frame_time * player.stat[player.role]['speed']
        pass

    def draw(self):
        self.image.clip_draw(int(self.frame) * 80, 0,80,80,self.x,self.y,)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 32., self.y - 20, self.x + 32, self.y + 20

    def handle_collision(self, group, other):
        if group == 'ball:sword':
            other.dir = math.atan2(other.y - self.y, other.x - self.x)
            other.x_dir = math.cos(other.dir) * self.power
            other.y_dir = math.sin(other.dir) * self.power
        pass