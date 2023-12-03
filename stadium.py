from pico2d import *

class Stadium:
    def __init__(self):
        self.stadium = load_image('resource/stadium/topview.png')
        self.sky = load_image('resource/stadium/sky.jpg')
        self.background = load_image('resource/stadium/backgrond.png')
        self.x = 800
        self.y = 450
        self.width = 1600
        self.height = 900

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        # self.background.draw(800,400,1600,900)
        self.sky.draw(800,600,1600,1200)
        self.background.draw(800,600,1600,1200)
        self.stadium.draw(self.x,self.y,self.width,self.height)
        # self.stadium.draw(800,300)
    def get_bb(self):
        return self.x - 681, self.y - 372, self.x + 687, self.y + 370

    def handle_collision(self, group, other):
        pass