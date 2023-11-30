import math

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import play_mode

machal = 1.02


class Ball:
    def __init__(self):
        self.x = 800
        self.y = 300
        self.x_dir = 0
        self.y_dir = 0
        self.image = load_image('resource/stadium/ball.png')

    def update(self):
        self.x += self.x_dir
        self.y += self.y_dir
        if self.x_dir < 0:
            self.x_dir /= machal
        elif self.x_dir > 0:
            self.x_dir /= machal
        if self.y_dir < 0:
            self.y_dir /= machal
        elif self.y_dir > 0:
            self.y_dir /= machal

        if self.x_dir < 0.0001 and self.x_dir > -0.0001:
            self.x_dir = 0
        if self.y_dir < 0.0001 and self.y_dir > -0.0001:
            self.y_dir = 0

    def draw(self):
        self.image.draw(self.x,self.y,64,64)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 32., self.y - 32, self.x + 32, self.y + 32

    def handle_collision(self, group, other):
        if group == 'stadium:ball':
            if self.x > 1455 :
                self.x_dir *= -1
                self.x = 1455
            elif self.x < 151:
                self.x_dir *= -1
                self.x = 151
            if self.y > 815:
                self.y_dir *= -1
                self.y = 815
            elif self.y < 85:
                self.y_dir *= -1
                self.y = 85