import time
from tkinter import *
import pygame,gym
from gym import spaces
import numpy as np
from tkinter import messagebox

class Ball:
    def __init__(self,canvas, color, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 15, 15, fill=color)
        self.canvas.move(self.id,x,y)
    def move(self,x,y):
        self.canvas.move(self.id, x, y)
class Platform:
    def __init__(self,canvas,color,x,y):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 15, fill=color)
        self.canvas.move(self.id,x,y)
        self.state = None
        self.score = 0
    def move(self,x,y):
        self.canvas.move(self.id, x, y)
class Bouns_area:
    def __init__(self,canvas,color,w,x,y):
        """
        :param canvas:
        :param color:
        :param w: 加分區長度
        :param x: 位置
        :param y: 位置
        """
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, w, 15, fill=color)
        self.canvas.move(self.id,x,y)
class Middleline:
    def __init__(self,canvas,window_W,window_H):
        self.canvas = canvas
        self.canvas.create_line(0,window_H/2,window_W,window_H/2,fill='black')
class Score:
    def __init__(self,canvas,x,y):
        self.canvas = canvas
        self.score = self.canvas.create_text(x,y,text = f'score:0',font=('Arial', 25))
        self.x = x
        self.y = y
    def update_score(self,s,Score):
        self.canvas.delete(s.score)
        self.score = self.canvas.create_text(self.x,self.y, text=f'score:{Score}',font=('Arial', 25))



class BouncyBall_Game(gym.Env):
    def __init__(self):
        self.tk = Tk()
        self.tk.title(f'bouncy ballv2')
        self.tk.wm_attributes('-topmost', 1)
        # self.tk.resizable(width=False, height=False)
        self.window_W = 640
        self.window_H = 800

        self.canvas = Canvas(self.tk, width=self.window_W, height=self.window_H)
        self.canvas.pack()
        m = Middleline(self.canvas, self.window_W, self.window_H)
        self.s1 = Score(self.canvas, self.window_W / 2, self.window_H * 0.25)
        self.s2 = Score(self.canvas, self.window_W / 2, self.window_H * 0.75)

        self.platform_up = Platform(self.canvas, 'green', self.window_W / 2 - 50, 5)
        self.platform_down = Platform(self.canvas, 'red', self.window_W / 2 - 50, self.window_H - 15)
        # self.canvas.create_text(50, self.window_H * 0.95, text=f'uping',font=('Arial', 15))

        self.speed = 0.5
        self.atk = None

        # self.action_space = spaces.Box(low=-2, high=2, shape=(1, ), dtype=np.float32)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=800, shape=(10,), dtype=np.float32)

        self.ball = Ball(self.canvas, 'yellow', 0, 0)
        self.ball_move_x = (np.random.random() * 2) - 1
        self.ball_move_y = 1
        self.ballpos = None

        self.rewardlst = []
        self.avgreward = []
        self.combolst = []
        self.reward = 0
        self.testtime = 0
        self.hit = 0  # 怕ball卡在板子裡面
        self.combo = 0
        self.done = False

        # net
        self.message = ''
        self.m_time = 0
        self.tk.update()

    def step(self, action, playing=False, act=''):
        self.done = False
        self.edge_judge()
        self.colliction_judge()
        self.get_score()
        self.playing = playing
        if action == 0:
            up_move_x = 5
            down_move_x = 5
        elif action == 1:
            up_move_x = 5
            down_move_x = -5
        elif action == 2:
            up_move_x = -5
            down_move_x = 5
        elif action == 3:
            up_move_x = -5
            down_move_x = -5
        self.ball.move(self.ball_move_x * self.speed, self.ball_move_y * self.speed)
        # net
        self.canvas.bind_all('<KeyPress-Right>', lambda event: self.send_to_server(event=event, message='Right'))
        self.canvas.bind_all('<KeyPress-Left>', lambda event: self.send_to_server(event=event, message='Left'))
        self.canvas.bind_all('<Key>', lambda event: self.send_to_server(event=event))
        # ---------------------------------------------------------------------------------
        if self.platformpos_up[0] < 0:
            self.platform_up.move(1, 0)
        elif self.platformpos_up[2] > self.window_W:
            self.platform_up.move(-1, 0)
        else:
            self.platform_up.move(up_move_x, 0)  # ;print(move_x)
        # ---------------------------------------------------------------------------------
        if self.playing == False:
            try:
                self.canvas.delete(self.t)
            except:
                pass
            self.t=self.canvas.create_text(self.window_W / 6, self.window_H * 0.85,text=f'Autoing...',font=('Arial', 25))
            if self.platformpos_down[0] < 0:
                self.platform_down.move(1, 0)
            elif self.platformpos_down[2] > self.window_W:
                self.platform_down.move(-1, 0)
            else:
                self.platform_down.move(down_move_x, 0)  # ;print(move_x)
        elif self.playing == True:
            try:
                self.canvas.delete(self.t)
            except:
                pass
            self.t=self.canvas.create_text(self.window_W / 6, self.window_H * 0.85,text=f'Manualing...',font=('Arial', 25))

            if act == 'Right' and self.platformpos_down[2] < self.window_W:
                self.move_x = 1
                self.platform_down.move(x=self.move_x, y=0)
            elif act == 'Left' and self.platformpos_down[0] > 0:
                self.move_x = -1
                self.platform_down.move(x=self.move_x, y=0)
        # ---------------------------------------------------------------------------------
        if self.platform_up.state == 'def':
            self.reward -= (abs((self.ballpos[0] + self.ballpos[2]) / 2 - (
                        self.platformpos_up[0] + self.platformpos_up[0]) / 2)) * 1e-6
        elif self.platform_down.state == 'def':
            self.reward -= (abs((self.ballpos[0] + self.ballpos[2]) / 2 - (
                        self.platformpos_down[0] + self.platformpos_down[0]) / 2)) * 1e-6
        # ---------------------------------------------------------------------------------
        self.tk.update()
        # ball
        self.ballpos = self.canvas.coords(self.ball.id)
        self.platformpos_up = self.canvas.coords(self.platform_up.id)
        self.platformpos_down = self.canvas.coords(self.platform_down.id)

        self.rewardlst.append(self.reward)
        # observation = np.array(self.ballpos + self.platformpos_up + self.platformpos_opponent)
        observation = self.get_obs(self.ballpos, self.platformpos_up, self.platformpos_down)
        if self.message != '':
            self.m_time += 1
            if self.m_time >= 50:
                self.m_time = 0
                self.message = ''
        return observation, self.reward, self.done, {}

    def edge_judge(self):
        if self.ballpos[0] < 0:
            self.ball_move_x *= -1
        if self.ballpos[2] > self.window_W:
            self.ball_move_x *= -1

    def get_score(self):
        if self.ballpos[1] <= self.platformpos_up[3] - 0.5:
            self.platform_down.score += 1
            self.s2.update_score(self.s2, self.platform_down.score)
            self.platform_down.state = 'def'
            self.platform_up.state = 'atk'
            self.done = True
        if self.ballpos[3] >= self.platformpos_down[1] + 0.5:
            self.platform_up.score += 1
            self.s1.update_score(self.s1, self.platform_up.score)
            self.platform_up.state = 'def'
            self.platform_down.state = 'atk'
            self.done = True

    def colliction_judge(self):
        # if self.ballpos[2] >= self.platformpos_up[0] and self.ballpos[0] <= self.platformpos_up[2]:
        #     if self.ballpos[3] >= self.platformpos_up[1] and self.ballpos[1] <= self.platformpos_up[3]:
        ballpos_x = (self.ballpos[0] + self.ballpos[2]) / 2
        if self.ballpos[2] >= self.platformpos_up[0] and self.ballpos[0] <= self.platformpos_up[2]:
            if self.ballpos[1] <= self.platformpos_up[3]:
                self.ball_move_x = (np.random.random() * 2) - 1
                self.ball_move_y *= -1
                self.platform_up.state = 'atk'
                self.platform_down.state = 'def'
                self.reward += (1 + self.combo * 0.5)
                self.combo += 1;
                print(f'ballpos:{self.ballpos},platformpos:{self.platformpos_up}')

        # if self.ballpos[2] >= self.platformpos_down[0] and self.ballpos[0] <= self.platformpos_down[2]:
        #     if self.ballpos[3] >= self.platformpos_down[1] and self.ballpos[1] <= self.platformpos_down[3]:
        if self.ballpos[2] >= self.platformpos_down[0] and self.ballpos[0] <= self.platformpos_down[2]:
            if self.ballpos[3] >= self.platformpos_down[1]:
                self.platform_up.state = 'def'
                self.platform_down.state = 'atk'
                self.ball_move_x = (np.random.random() * 2) - 1
                self.ball_move_y *= -1
                self.reward += (1 + self.combo * 0.5)
                self.combo += 1;
                print(f'ballpos:{self.ballpos},platformpos:{self.platformpos_down}')

    def get_obs(self, ballpos, up_pos, down_pos):
        ballposx = (ballpos[0] + ballpos[2]) / 2
        ballposy = (ballpos[1] + ballpos[3]) / 2
        up_posx = (up_pos[0] + up_pos[2]) / 2
        up_posy = (up_pos[1] + up_pos[3]) / 2

        down_posx = (down_pos[0] + down_pos[2]) / 2
        down_posy = (down_pos[1] + down_pos[3]) / 2  # down

        up_dis = np.linalg.norm(np.array([ballposx, ballposy]) - np.array([up_posx, up_posy]))
        down_dis = np.linalg.norm(np.array([ballposx, ballposy]) - np.array([down_posx, down_posy]))

        upstate = 1 if self.platform_up.state == 'atk' else 0
        downstate = 1 if self.platform_down.state == 'atk' else 0

        return np.array(
            [up_posx, up_posy, down_posx, down_posy, ballposx, ballposy, up_dis, down_dis, upstate, downstate])

    def reset(self):
        self.canvas.delete(self.ball.id)
        m = Middleline(self.canvas, self.window_W, self.window_H)
        self.atk = np.random.choice(['up', 'down'])

        if self.atk == 'up':
            self.platformpos_up = self.canvas.coords(self.platform_up.id)
            self.platformpos_down = self.canvas.coords(self.platform_down.id)
            ball_x = (self.platformpos_up[0] + self.platformpos_up[2]) / 2
            ball_y = self.platformpos_up[3]
            self.ball = Ball(self.canvas, 'yellow', ball_x, ball_y + 15)
            self.platform_up.state = 'atk'
            self.platform_down.state = 'def'
            self.ball_move_x = (np.random.random() * 2) - 1
            self.ball_move_y = 1
        else:
            self.platformpos_up = self.canvas.coords(self.platform_up.id)
            self.platformpos_down = self.canvas.coords(self.platform_down.id)
            ball_x = (self.platformpos_down[0] + self.platformpos_down[2]) / 2
            ball_y = self.platformpos_down[1]
            self.ball = Ball(self.canvas, 'yellow', ball_x, ball_y - 20)
            self.platform_up.state = 'def'
            self.platform_down.state = 'atk'
            self.ball_move_x = (np.random.random() * 2) - 1
            self.ball_move_y = -1

        self.ballpos = self.canvas.coords(self.ball.id)
        self.reward = 0
        self.testtime += 1;
        print('testtime:', self.testtime)
        avg = np.mean(self.rewardlst)
        self.avgreward.append(avg);
        print(f'avg reward:{avg}')
        self.rewardlst = []
        try:
            self.combolst.append(self.combo);
            print('combo:', self.combo)

        except:
            pass
        self.combo = 0
        print(self.atk)
        obs = self.get_obs(self.ballpos, self.platformpos_up, self.platformpos_down)
        return obs

    def send_to_server(self, event, message=''):
        if event.char == 'a':
            self.message = 'Auto'
        elif event.char == 'm':
            self.message = 'Manual'
        elif event.char == 'p':
            self.message = 'Music'
        else:
            self.message = message

    def render(self, mode='human', clode=False):
        pass

    def close(self):
        self.tk.destroy()

class Login:
    def __init__(self):
        self.tk = Tk()
        self.tk.title(f'Login')
        self.tk.wm_attributes('-topmost', 2)
        self.tk.resizable(width=False, height=False)
        self.window_W = 200
        self.window_H = 200
        self.canvas = Canvas(self.tk, width=self.window_W, height=self.window_H)
        self.canvas.pack()

        self.tk.update()
        self.b1 = Ball(self.canvas, 'blue', 50, 50)


        lbltitle = Label(text='Bouncy Ball', font=10)
        lbltitle.place(x=self.window_W / 2, y=self.window_H / 5, anchor='center')
        self.startbtn = Button(self.tk, width=20, text='start',
                               command=lambda: [self.send_to_server(message='Start'), self.close()])
        self.startbtn.place(x=self.window_W / 2, y=self.window_H * 4 / 5, anchor='center')
        self.message = ''
        self.ball_move_x = np.random.random() / 20
        self.ball_move_y = np.random.random() / 20

    def close(self):
        messagebox.showinfo("遊戲規則", "1.按左右鍵讓平台往左或往右\n\n2.遊戲難度偏高(我故意的),受不了可以按a(挑戰自我可以按m切回手動操控)\n\n3.按p可以播放/停止音樂")
        try:
            self.tk.destroy()
        except Exception as e:
            print(e)

    def keyinput(self):
        self.tk.update()
        self.edge_judge(self.b1)

    def edge_judge(self, ball):
        ball.move(self.ball_move_x, self.ball_move_y)
        ballpos = self.canvas.coords(ball.id)
        if ballpos[0] < 0:
            self.ball_move_x *= -1
        if ballpos[1] < 0:
            self.ball_move_y *= -1
        if ballpos[2] > self.window_W:
            self.ball_move_x *= -1
        if ballpos[3] > self.window_H:
            self.ball_move_y *= -1

    def send_to_server(self, message=''):
        self.message = message
if __name__=='__main__':
    from sb3_contrib.qrdqn import QRDQN
    model = QRDQN.load("./model/qrdqn_BouncyBallv2")
    env = BouncyBall_Game()
    obs = env.reset()
    while True:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action, playing=False)
        if done:
            obs = env.reset()


