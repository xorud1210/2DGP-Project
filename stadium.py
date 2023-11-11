from pico2d import *

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Stadium:
    def __init__(self):
        self.stadium = load_image('resource/stadium/topview.png')
        # self.background = load_image('resource/stadium/backgrond.png')
        # self.camera_pos = 0;
        # self.camera_dir = 0;
        self.x = 800
        self.y = 450
        self.width = 1600
        self.height = 900

    def update(self):
        # self.camera_pos += self.camera_dir * 5
        pass

    def handle_event(self, event):
        pass
        # if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
        #     self.camera_dir -= 1
        # elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
        #     self.camera_dir += 1
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
        #     self.camera_dir += 1
        # elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
        #     self.camera_dir -= 1

    def draw(self):
        # self.background.draw(800,400,1600,900)
        self.stadium.draw(self.x,self.y,self.width,self.height)
        draw_rectangle(*self.get_bb())
        # self.stadium.draw(800,300)
    def get_bb(self):
        return self.x - 681, self.y - 372, self.x + 687, self.y + 370

    def handle_collision(self, group, other):
        pass