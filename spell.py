
from pico2d import load_image, draw_rectangle, load_wav

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

class Spell:
    def __init__(self, x, y, power, x_dir=0, y_dir=0):
        self.x = x + x_dir * 5 * PIXEL_PER_METER
        self.y = y + y_dir * 5 * PIXEL_PER_METER
        self.first_x = x
        self.first_y = y
        self.power = power
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.speed = 1
        self.range = 5 * PIXEL_PER_METER
        self.image = load_image('resource/vfx/spell.png')
        self.frame = 0
        self.sound = load_wav('resource/sound/spell2.wav')
        self.sound.set_volume(64)
        self.sound.play()
        game_world.add_collision_pair('ball:spell', None, self)

    def update(self):
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if (self.x - self.first_x) ** 2 + (self.y - self.first_y) ** 2 < 0.5 * PIXEL_PER_METER:
            game_world.remove_object(self)
        self.x += -self.x_dir * RUN_SPEED_PPS * game_framework.frame_time * self.speed
        self.y += -self.y_dir * RUN_SPEED_PPS * game_framework.frame_time * self.speed

    def draw(self):
        if self.x_dir > 0:
            self.image.clip_draw(int(self.frame) % 5 * 63, 0,63,110,self.x,self.y,30,60)
        else:
            self.image.clip_composite_draw(int(self.frame) % 5 * 63, 0,63,110,0,'h',self.x,self.y,30,60)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15., self.y - 30, self.x + 15, self.y + 30

    def handle_collision(self, group, other):
        if group == 'ball:spell':
            other.dir = math.atan2(other.y - self.y, other.x - self.x)
            other.x_dir = math.cos(other.dir) * self.power
            other.y_dir = math.sin(other.dir) * self.power
            game_world.remove_object(self)
