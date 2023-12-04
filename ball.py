import math

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import play_mode

machal = 1.02


class Ball:
    def __init__(self):
        self.x = 800
        self.y = 450
        self.x_dir = 0
        self.y_dir = 0
        self.ball = load_image('resource/stadium/ball.png')
        self.fever_ball = load_image('resource/stadium/fever_ball.png')

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
        # 필드 벽과 충돌
        if self.x > 1455:
            if self.y > 350 and self.y < 550:
                pass
            else:
                self.x_dir *= -1
                self.x = 1455
        elif self.x < 151:
            if self.y > 350 and self.y < 550:
                pass
            else:
                self.x_dir *= -1
                self.x = 151
        if self.y > 815:
            self.y_dir *= -1
            self.y = 815
        elif self.y < 85:
            self.y_dir *= -1
            self.y = 85

    def draw(self):
        if play_mode.scoreboard.fever:
            self.fever_ball.draw(self.x, self.y, 64, 64)
        else:
            self.ball.draw(self.x, self.y, 64, 64)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 32., self.y - 32, self.x + 32, self.y + 32

    def handle_collision(self, group, other):
        pass

    def respawn(self):
        self.x = 800
        self.y = 450
        self.x_dir = 0
        self.y_dir = 0