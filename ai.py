import math

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image

import game_framework
import play_mode
from arrow import Arrow
from orb import Orb
from sword import Sword

# player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Ai:
    def __init__(self):
        self.x, self.y = 800, 300
        self.frame = 0
        self.action = 9
        self.x_dir = 0
        self.y_dir = 0
        self.dir = 0.0
        self.run = False
        self.frame_wid = 128
        self.frame_hei = 128
        self.max_frame = 6
        self.speed = 1.5
        self.attack_speed = 0.6
        self.role = 'knight'
        self.stat = {'knight': {'power': 2, 'speed': 1.5, 'attack_speed': 0.6, 'weapon': Sword},
                     'wizard': {'power': 4, 'speed': 1, 'attack_speed': 0.5, 'weapon': Orb},
                     'archer': {'power': 6, 'speed': 1.2, 'attack_speed': 1.5, 'weapon': Arrow}}
        self.image = {'knight': load_image('resource/player/knight.png'),
                      'wizard': load_image('resource/player/wizard.png'),
                      'archer': load_image('resource/player/archer.png')}
        self.sprite = {
            'knight': {'max_frame': {'idle': 6, 'walk': 8, 'run': 7, 'atk1': 5, 'atk2': 2, 'atk3': 3, 'atk4': 4},
                       'action': {'idle': 9, 'walk': 8, 'run': 7, 'atk1': 6, 'atk2': 5, 'atk3': 4, 'atk4': 3}},
            'wizard': {'max_frame': {'idle': 6, 'walk': 7, 'run': 8, 'atk1': 10, 'atk2': 4, 'atk3': 7},
                       'action': {'idle': 9, 'walk': 8, 'run': 7, 'atk1': 5, 'atk2': 4, 'atk3': 3}},
            'archer': {'max_frame': {'idle': 6, 'walk': 8, 'run': 8, 'atk1': 14, 'atk2': 13, 'atk3': 4},
                       'action': {'idle': 9, 'walk': 8, 'run': 7, 'atk1': 5, 'atk2': 4, 'atk3': 3}},
        }
        self.input_time = 0

        self.build_behavior_tree()

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.max_frame
        self.bt.run()

    def draw(self):
        if math.cos(self.dir) < 0:
            self.image[self.role].clip_composite_draw(int(self.frame) * self.frame_wid,
                                                          self.action * self.frame_hei, self.frame_wid,
                                                          self.frame_hei, 0, 'h',
                                                          self.x, self.y + 25, self.frame_wid,
                                                          self.frame_hei)
        else:
            self.image[self.role].clip_draw(int(self.frame) * self.frame_wid,
                                            self.action * self.frame_hei, self.frame_wid,
                                            self.frame_hei, self.x, self.y + 25,
                                            self.frame_wid, self.frame_hei)

    def handle_event(self, event):
        pass

    def state_change(self, state):
        self.action = self.sprite[self.role]['action'][state]
        self.max_frame = self.sprite[self.role]['max_frame'][state]

    def set_dir(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.x_dir = 1 if math.cos(self.dir) > 0 else -1
        self.y_dir = 1 if math.sin(self.dir) > 0 else -1

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_to_ball(self, r=1):
        self.state_change('walk')
        self.set_dir(play_mode.ball.x, play_mode.ball.y)
        self.speed = RUN_SPEED_PPS * self.stat[self.role]['speed']
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

        if self.distance_less_than(play_mode.ball.x,play_mode.ball.y,self.x,self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        a1 = Action('Move to ball',self.move_to_ball)
        SEQ_move_to_ball = Sequence('Move to ball', a1)

        root = SEQ_move_to_ball

        self.bt = BehaviorTree(root)
