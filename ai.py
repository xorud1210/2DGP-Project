import math
import random

import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image, get_time

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
        self.x, self.y = 1200, 300
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
        self.stat = {'knight': {'power': 2, 'range': 1.2, 'speed': 1.5, 'attack_speed': 0.6, 'weapon': Sword},
                     'wizard': {'power': 4, 'range': 12, 'speed': 1, 'attack_speed': 0.5, 'weapon': Orb},
                     'archer': {'power': 6, 'range': 8, 'speed': 1.2, 'attack_speed': 1.5, 'weapon': Arrow}}
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

    def thinking(self):
        if get_time() - self.time <game_framework.frame_time * 1000:
            return BehaviorTree.RUNNING
        else:
            return BehaviorTree.SUCCESS

    def set_dir(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.x_dir = 1 if math.cos(self.dir) > 0 else -1
        self.y_dir = 1 if math.sin(self.dir) > 0 else -1

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_to_ball(self):
        self.state_change('walk')
        self.set_dir(play_mode.ball.x, play_mode.ball.y)
        self.speed = RUN_SPEED_PPS * self.stat[self.role]['speed']
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

        if self.distance_less_than(play_mode.ball.x,play_mode.ball.y,self.x,self.y, self.stat[self.role]['range']):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def select_weapon(self):
        roles = ['knight', 'wizard', 'archer']
        self.role = roles[random.randint(0,2)]

        return BehaviorTree.SUCCESS

    def can_attack(self):
        if self.distance_less_than(play_mode.ball.x,play_mode.ball.y,self.x,self.y, self.stat[self.role]['range']):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def cant_attack(self):
        if self.distance_less_than(play_mode.ball.x,play_mode.ball.y,self.x,self.y, self.stat[self.role]['range']):
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def attack(self):
        self.state_change('atk1')
        weapon = self.stat[self.role]['weapon'](self.x + 40 * self.x_dir, self.y + 40 * self.y_dir, self.stat[self.role]['power'],
                                                self.x_dir, self.y_dir)
        if self.frame < self.max_frame - 0.05:
            return BehaviorTree.RUNNING
        else:
            game_world.add_object(weapon)
            self.time = get_time()
            return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
        a1 = Action('Weapon Select', self.select_weapon)
        SEQ_select_weapon = Sequence('무기 고르기', a1)

        c1 = Condition('공이 사거리 내에 있나?', self.can_attack)
        a2 = Action('공격',self.attack)
        a4 = Action('생각 중',self.thinking)
        SEQ_attack = Sequence('공 때리기', c1, a2, a1, a4)

        c2 = Condition('공이 사거리 보다 멀리 있나?', self.cant_attack)
        a3 = Action('Move to ball',self.move_to_ball)
        SEQ_move_to_ball = Sequence('Move to ball',  c2, a3)

        root = SEL_attack_or_move = Selector('공격 혹은 이동', SEQ_attack, SEQ_move_to_ball)

        # root = Selector('무기 선택 및 행동', SEQ_select_weapon, SEL_attack_or_move)

        self.bt = BehaviorTree(root)
