from pico2d import load_font, load_image, get_time

import play_mode


class Scoreboard:
    def __init__(self):
        self.x = 790
        self.y = 1000
        self.left_score = 0
        self.right_score = 0
        self.font = load_font('ENCR10B.TTF', 50)
        self.image = load_image('resource/stadium/scoreboard.png')
        self.time = get_time()
        self.last_time = get_time()
        self.fever = False

    def update(self):
        cur_time = get_time()
        self.time += cur_time - self.last_time
        self.last_time = cur_time
        if self.time > 50:
            self.fever = True
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 800, 600)
        self.font.draw(self.x - 60,self.y, f'{self.left_score}', (255,255,255))
        self.font.draw(self.x + 50,self.y, f'{self.right_score}', (255, 255, 255))
        if self.fever:
            self.font.draw(self.x - 40, self.y - 60, f'{round(self.time, 2)}', (255, 0, 0))
        else:
            self.font.draw(self.x - 40,self.y - 60, f'{round(self.time, 2)}', (0, 0, 0))


