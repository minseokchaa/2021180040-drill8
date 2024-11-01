from pico2d import load_image, get_time

from state_machine import StateMachine, time_out,  right_down, left_down, a_down, start_event


# 상태를 클래스를 통해서 정의함
class Idle:
    @staticmethod  # @는 데코레이터라는 기능, 클래스 안에 들어있는 객채하곤 상관이 없는 함수, 모아 놓는 개념?
    def enter(boy,e):
        if boy.face_dir == 1:
            boy.action = 3

        elif boy.face_dir == -1:
            boy.action = 2
        boy.frame = 0
        boy.dir = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

        pass

class Run:
    @staticmethod
    def enter(boy,e):

        if right_down(e):
             boy.dir,boy.action = 1, 1
        elif left_down(e):
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

        if boy.x + boy.dir*5 > 800: #왼쪽으로 방향 전환
            boy.dir = -1
            boy.face_dir =-1
            boy.action = 0

        if boy.x + boy.dir*5 < 0:   #오른쪽으로 방향전환
            boy.dir = 1
            boy.face_dir = 1
            boy.action = 1
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y
        )
        pass

class AutoRun:
    @staticmethod
    def enter(boy, e):
        boy.start_time = get_time()

        if boy.face_dir ==1:
            boy.dir = 1
            boy.action = 1
        if boy.face_dir == -1:
            boy.dir = -1
            boy.action = 0

        boy.frame = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 10
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT',0))

        if boy.x + boy.dir*5 > 800: #왼쪽으로 방향 전환
            boy.dir = -1
            boy.face_dir =-1
            boy.action = 0

        if boy.x + boy.dir*5 < 0:   #오른쪽으로 방향전환
            boy.dir = 1
            boy.face_dir = 1
            boy.action = 1
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y+20,150,150
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
                Run: {},                        #run상태에서 어떠한 이벤트가 들어와도 처리하지 않겠다.
                Idle : {a_down: AutoRun},
                AutoRun: {right_down: Run, left_down: Run, time_out: Idle}
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
