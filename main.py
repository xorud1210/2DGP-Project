from pico2d import open_canvas, delay, close_canvas
import game_framework

import title_mode as start_mode

open_canvas(1600, 1200)
game_framework.run(start_mode)
close_canvas()

