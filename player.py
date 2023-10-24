from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:
    @staticmethod
    def enter(player, e):
        player.dir = 0
        player.frame = 0
        player.wait_time = get_time()

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 3
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 102, player.action * 162, 102, 162, player.x, player.y)
        pass


class Walk:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.action = 1, 0
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.action = -1, 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 3
        player.x += player.dir * 5
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 102, player.action * 162, 102, 162, player.x, player.y)
        pass
    pass


class Sleep:
    pass


class Player:
    def __init__(self):
        self.x, self.y = 200, 300
        self.frame = 0
        self.action = 0
        self.dir = 0
        self.image = load_image('resource/player/player.png')
        self.state_machine = StateMachine(self)

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        pass


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Idle, right_down: Walk, left_down: Walk, left_up: Walk, right_up: Walk, time_out: Sleep},
            Walk: {space_down: Walk, right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Sleep: {right_down: Walk, left_down: Walk, right_up: Walk, left_up: Walk}}

    def start(self):
        self.cur_state.enter(self.player)

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.player)
