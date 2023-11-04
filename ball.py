from pico2d import load_image, draw_rectangle

import game_world
import play_mode


class Ball:
    def __init__(self):
        self.x = 800
        self.y = 300
        self.x_dir = 0
        self.y_dir = 0
        self.image = load_image('resource/stadium/ball.png')

    def update(self):
        self.x += self.x_dir * 4
        self.y += self.y_dir * 3
        if self.x_dir < 0:
            self.x_dir += 0.05
        elif self.x_dir > 0:
            self.x_dir -= 0.05
        if self.y_dir < 0:
            self.y_dir += 0.05
        elif self.y_dir > 0:
            self.y_dir -= 0.05

    def draw(self):
        self.image.draw(self.x,self.y,64,64)
        draw_rectangle(*self.get_bb())


