from pico2d import load_font

import play_mode


class Score:
    def __init__(self):
        self.left_score = 0
        self.right_score = 0
        self.font = load_font('ENCR10B.TTF', 40)

    def update(self):
        pass

    def draw(self):
        self.font.draw(play_mode.left_goalpost.x,play_mode.left_goalpost.y, f'{self.left_score}', (0,0,0))
        self.font.draw(play_mode.right_goalpost.x, play_mode.right_goalpost.y, f'{self.right_score}', (0, 0, 0))

