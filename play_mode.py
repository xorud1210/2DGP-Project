import random

from pico2d import *
import game_framework

import game_world
from player import Player
from stadium import Stadium
from ball import Ball
# from grass import Grass
# from boy import Boy
# from ball import Ball
# from zombie import Zombie

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)
            stadium.handle_event(event)

def init():
    global player
    global stadium
    global ball

    running = True

    stadium = Stadium()
    game_world.add_object(stadium, 0)

    player = Player()
    game_world.add_object(player, 1)

    ball = Ball()
    game_world.add_object(ball, 1)
    # fill here

    game_world.add_collision_pair('player:ball',player,ball)
    game_world.add_collision_pair('stadium:ball',stadium,ball)
    game_world.add_collision_pair('stadium:player', stadium, player)




def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    # fill here

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

