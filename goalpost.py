from pico2d import draw_rectangle

import play_mode


class Goalpost:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        pass
    def get_bb(self):
        return self.x - 10., self.y - 70, self.x + 10, self.y + 65

    def handle_collision(self, group, other):
        if group == 'leftgoal:ball':
            play_mode.score.left_score += 1
            play_mode.ball.respawn()
        elif group == 'rightgoal:ball':
            play_mode.score.right_score += 1
            play_mode.ball.respawn()



