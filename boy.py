from pico2d import load_image, get_time

from state_machine import StateMachine, space_down, time_out, right_down, left_down, left_up, right_up, start_event


# 상태를 클래스를 통해서 정의함
class Idle:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(boy,e):
        boy.start_time = get_time()
        if right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 2:
            boy.state_machine.add_event(('TIME_OUT',0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

        pass

class Sleep:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):
             boy.dir,boy.action = 1, 1
        elif left_down(e) or right_up(e):
            boy.dir, boy.action = -1, 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir ==1:
            boy.image.clip_composite_draw(
                boy.frame *100, 300, 100, 100,
                3.141592/2, # 90도 회전
                '', # 좌우상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )
        elif boy.face_dir ==-1:
            boy.image.clip_composite_draw(
                boy.frame *100, 200, 100, 100,
                -3.141592/2, # 90도 회전
                '', # 좌우상하 반전 X
                boy.x+25 , boy.y-25 , 100, 100
            )

class Run:
    @staticmethod
    def enter(boy,e):

        if right_down(e) or left_up(e):
             boy.dir,boy.action = 1, 1
        elif left_down(e) or right_up(e):
            boy.dir, boy.action = -1, 0
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir*5
        boy.frame = (boy.frame+1)%8
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y
        )
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.start_time = get_time()
        self.state_machine = StateMachine(self) #소년 객체의 state machine 생성
        self.state_machine.start(Idle)      #초기 상태 -- Idle
        self.state_machine.set_transitions(
            {
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},    #run상태에서 어떠한 이벤트가 들어와도 처리하지 않겠다.
                Idle : {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out : Sleep},
                Sleep : {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle}
            }
        )


    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        #event: 입력 이벤트 key mouse
        #우리가 state_machine에 전달해 줄건 ( , )
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
