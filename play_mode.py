import random

from pico2d import *
import game_framework

import game_world
from goalpost import Goalpost
from player import Player
from score import Score
from stadium import Stadium
from ball import Ball
from ai import Ai
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
    global ai
    global left_goalpost, right_goalpost
    global score

    running = True

    stadium = Stadium()
    game_world.add_object(stadium, 0)

    player = Player()
    game_world.add_object(player, 1)

    ball = Ball()
    game_world.add_object(ball, 1)

    ai = Ai()
    game_world.add_object(ai,1)
    # fill here

    left_goalpost = Goalpost(85,450)
    game_world.add_object(left_goalpost, 0)

    right_goalpost = Goalpost(1520,450)
    game_world.add_object(right_goalpost, 0)

    score = Score()
    game_world.add_object(score,0)

    game_world.add_collision_pair('player:ball',player,ball)
    game_world.add_collision_pair('leftgoal:ball',left_goalpost,ball)
    game_world.add_collision_pair('rightgoal:ball',right_goalpost,ball)

    game_world.add_collision_pair('ball:sword',ball,None)
    game_world.add_collision_pair('ball:orb',ball,None)
    game_world.add_collision_pair('ball:arrow',ball,None)


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

