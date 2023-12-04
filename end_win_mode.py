from pico2d import *
import game_framework
import game_world
import play_mode
import title_mode


def init():
    global bg_iamge
    global press_space
    global time
    global bgm
    global key_sound

    bg_iamge = load_image('resource/title/you_win.jpg')
    press_space = load_image('resource/title/restart.png')
    time = get_time()
    bgm = load_music('resource/sound/win.mp3')
    bgm.set_volume(64)
    bgm.play()
    key_sound = load_wav('resource/sound/press_key.wav')
    key_sound.set_volume(64)

    game_world.clear()

def finish():
    global bg_iamge
    global press_space
    global time
    global bgm

    del bg_iamge
    del press_space
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
            game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    bg_iamge.draw(800, 600, 1600, 1200)
    if int(time) % 2 != 0:
        press_space.draw(800,200)
    update_canvas()

def update():
    global time
    time = get_time()
    pass

def pause():
    pass

def resume():
    pass