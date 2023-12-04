from pico2d import *
import game_framework
import manual_mode
import play_mode
def init():
    global manual

    manual = load_image('resource/title/manual.png')

def finish():
    global manual

    del manual

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.pop_mode()

def draw():
    manual.draw(800,400)
    update_canvas()

def update():
    global time
    time = get_time()
    pass

def pause():
    pass

def resume():
    pass