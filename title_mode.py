from pico2d import *
import game_framework
import manual_mode
import play_mode
def init():
    global bg_image
    global press_space
    global press_m
    global time
    global bgm
    global key_sound

    bg_image = load_image('resource/title/title.png')
    press_space = load_image('resource/title/press_space.png')
    press_m = load_image('resource/title/press_m.png')
    time = get_time()
    bgm = load_music('resource/sound/title.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()
    key_sound = load_wav('resource/sound/press_key.wav')
    key_sound.set_volume(64)

def finish():
    global bg_image
    global press_space
    global press_m
    global time
    global bgm

    del bg_image
    del press_space
    del press_m
    del time
    del bgm

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            key_sound.play()
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_m:
            game_framework.push_mode(manual_mode)

def draw():
    clear_canvas()
    bg_image.draw(800, 600, 1600, 1200)
    if int(time) % 3 != 0:
        press_space.draw(800,800,400,200)
    press_m.draw(1600 - 120, 1200 - 25)
    update_canvas()

def update():
    global time
    time = get_time()
    pass

def pause():
    pass

def resume():
    pass