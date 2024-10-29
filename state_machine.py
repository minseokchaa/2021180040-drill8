#이벤트 체크 함수를 정의
# 상태이벤트 e = (종류, 실제 값) 튜플로 정의
from tabnanny import check

from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

def start_event(e):
    return e[0] == 'START'
    pass

def space_down(e):       # e가 space down 인지 판단? true or false
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key ==SDLK_SPACE

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def time_out(e):         #e가 time out인지 판단
    return e[0] == 'TIME_OUT'




class StateMachine:
    def __init__(self, obj):
        self.obj = obj #어떤 객체를 위한 상태머신인지 알려줌
        #상태 이벤트를 보관할 q
        self.event_q = []
        pass
    def start(self, state):
        self.cur_state = state  #시작 상태를 받아서, 그걸로 현재 상태에 입력
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'Enter into {state}')
        pass
    def update(self):
        self.cur_state.do(self.obj)     #Idle.do()
        #혹시 이텐트가 있나요?
        if self.event_q:    #list는 멤버가 있으면 true
            e = self.event_q.pop(0)
            # 이 시점에서 우리에게 주어진 정보는? == e, cur_state
            # 상태변환 테이블을 사용한다,
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):  #
                    print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj, e)
                    self.cur_state = next_state
                    print(f'Enter into {next_state}')
                    self.cur_state.enter(self.obj, e)
                    return      #제대로 이벤트에 대한 상태 변환 완료
            #이 시점으로 왔다는 것은, event에 따른 전환 못함
            print(f'        WARNING: {e} not handled at state {self.cur_state}')


        pass
    def draw(self):
        self.cur_state.draw(self.obj)
        pass
    def add_event(self, e):
        self.event_q.append(e)
        print(f'    DEBUG: add event{e}')
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass