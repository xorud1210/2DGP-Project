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
        if group == 'player:ball':
            self.x_dir = (self.x - other.x) / 50
            self.y_dir = (self.y - other.y) / 50
            print(self.x_dir,self.y_dir)
