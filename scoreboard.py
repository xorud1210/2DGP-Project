from pico2d import load_font, load_image, get_time, load_wav

import end_lose_mode
import end_win_mode
import game_framework
import play_mode


class Scoreboard:
    def __init__(self):
        self.x = 790
        self.y = 1000
        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5
        self.font = load_font('resource/font/font.ttf', 50)
        self.image = load_image('resource/stadium/scoreboard.png')
        self.fever_sound = load_wav('resource/sound/fever_bell.wav')
        self.fever_sound.set_volume(64)
        self.time = 0
        self.last_time = get_time()
        self.fever = False

    def update(self):
        cur_time = get_time()
        self.time += cur_time - self.last_time
        self.last_time = cur_time
        if self.time > 50 and not self.fever:
            self.fever = True
            self.fever_sound.play()
        if self.player_score >= self.target_score:
            game_framework.change_mode(end_win_mode)
        elif self.ai_score >= self.target_score:
            game_framework.change_mode(end_lose_mode)
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 800, 600)
        self.font.draw(self.x - 60, self.y, f'{self.player_score}', (255, 255, 255))
        self.font.draw(self.x + 50, self.y, f'{self.ai_score}', (255, 255, 255))
        if self.fever:
            self.font.draw(self.x - 40, self.y - 60, f'{round(self.time, 2)}', (255, 0, 0))
        else:
            self.font.draw(self.x - 40,self.y - 60, f'{round(self.time, 2)}', (0, 0, 0))


