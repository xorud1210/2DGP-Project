from pico2d import draw_rectangle, get_time, load_wav

import game_world
import play_mode


class Goalpost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.whistle = load_wav('resource/sound/whistle.wav')
        self.whistle.set_volume(64)

    def update(self):
        pass

    def draw(self):
        pass
    def get_bb(self):
        return self.x - 10., self.y - 70, self.x + 10, self.y + 65

    def handle_collision(self, group, other):
        if group == 'leftgoal:ball':
            play_mode.scoreboard.ai_score += 1
            play_mode.ball.respawn()
            play_mode.player.respawn()
            play_mode.ai.respawn()
            play_mode.scoreboard.time = 0
            play_mode.scoreboard.fever = False
            self.whistle.play()
        elif group == 'rightgoal:ball':
            play_mode.scoreboard.player_score += 1
            play_mode.ball.respawn()
            play_mode.player.respawn()
            play_mode.ai.respawn()
            play_mode.scoreboard.time = 0
            play_mode.scoreboard.fever = False
            self.whistle.play()
