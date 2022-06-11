from tkinter import *
import gym
from gym import spaces
import numpy as np
from src import Ball,Platform,Middleline,Score

class Bouncy_ballv1(gym.Env):
    def __init__(self):
        self.tk=Tk()
        self.tk.title(f'bouncy ballv2')
        self.tk.wm_attributes('-topmost',1)
        #self.tk.resizable(width=False, height=False)
        self.window_W = 640
        self.window_H = 800

        self.canvas=Canvas(self.tk,width=self.window_W,height=self.window_H)
        self.canvas.pack()
        m=Middleline(self.canvas,self.window_W,self.window_H)
        # self.canvas.create_line(0,self.window_H/2,self.window_W,self.window_H/2,fill='black')
        self.s1=Score(self.canvas,self.window_W / 2, self.window_H * 0.25)
        self.s2=Score(self.canvas,self.window_W / 2, self.window_H * 0.75)
        self.tk.update()

        self.platform_up = Platform(self.canvas,'green',self.window_W/2-50,5)
        self.platform_down = Platform(self.canvas,'red',self.window_W/2-50,self.window_H-15)
        # self.canvas.create_text(50, self.window_H * 0.95, text=f'uping',font=('Arial', 15))

        self.speed = 0.5
        self.atk = None

        #self.action_space = spaces.Box(low=-2, high=2, shape=(1, ), dtype=np.float32)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0,high=800,shape=(6, ), dtype=np.float32)

        self.ball = Ball(self.canvas, 'yellow', 0, 0)
        self.ball_move_x=(np.random.random()*2)-1
        self.ball_move_y=1
        self.ballpos = None

        self.rewardlst = []
        self.avgreward = []
        self.combolst = []
        self.reward=0
        self.testtime=0
        self.hit = 0 #怕ball卡在板子裡面
        self.combo = 0
        self.done = False

    def step(self, action, playing = False):
        self.done=False
        self.edge_judge()
        self.colliction_judge()
        self.get_score()
        if action==0:
            move_x = 5
        elif action==1:
            move_x = 0
        elif action==2:
            move_x = -5

        self.ball.move(self.ball_move_x * self.speed, self.ball_move_y * self.speed)
        # ---------------------------------------------------------------------------------
        if self.platform_up.state=='def':
            if self.platformpos_up[0] < 0:
                self.platform_up.move(1, 0)
            elif self.platformpos_up[2] > self.window_W:
                self.platform_up.move(-1, 0)
            else:
                self.platform_up.move(move_x, 0)  # ;print(move_x)
        # ---------------------------------------------------------------------------------
        elif self.platform_down.state == 'def':
            if self.platformpos_down[0] < 0:
                self.platform_down.move(1, 0)
            elif self.platformpos_down[2] > self.window_W:
                self.platform_down.move(-1, 0)
            else:
                self.platform_down.move(move_x, 0)  # ;print(move_x)
        # ---------------------------------------------------------------------------------
        if self.platform_up.state=='def':
            self.reward -= (abs((self.ballpos[0]+self.ballpos[2])/2-(self.platformpos_up[0]+self.platformpos_up[0])/2))*1e-6
        elif self.platform_down.state=='def':
            self.reward -= (abs((self.ballpos[0]+self.ballpos[2])/2-(self.platformpos_down[0]+self.platformpos_down[0])/2))*1e-6
        # ---------------------------------------------------------------------------------
        self.tk.update()
        # ball
        self.ballpos = self.canvas.coords(self.ball.id)
        self.platformpos_up = self.canvas.coords(self.platform_up.id)
        self.platformpos_down = self.canvas.coords(self.platform_down.id)


        self.rewardlst.append(self.reward)
        if self.platform_down.state=='def':
            observation = self.get_obs(self.ballpos,self.platformpos_down)
        elif self.platform_up.state=='def':
            observation = self.get_obs(self.ballpos,self.platformpos_up)
        return observation, self.reward, self.done, {}

    def edge_judge(self):
        if self.ballpos[0] < 0:
            self.ball_move_x *= -1
        if self.ballpos[2] > self.window_W:
            self.ball_move_x *= -1

    def get_score(self):
        if self.ballpos[1] <= self.platformpos_up[3]-0.5:
            self.platform_down.score += 1
            self.s2.update_score(self.s2,self.platform_down.score)
            self.platform_down.state = 'def'
            self.platform_up.state = 'atk'
            self.done=True
        if self.ballpos[3] >= self.platformpos_down[1]+0.5:
            self.platform_up.score += 1
            self.s1.update_score(self.s1,self.platform_up.score)
            self.platform_up.state = 'def'
            self.platform_down.state = 'atk'
            self.done=True

    def colliction_judge(self):
        # if self.ballpos[2] >= self.platformpos_up[0] and self.ballpos[0] <= self.platformpos_up[2]:
        #     if self.ballpos[3] >= self.platformpos_up[1] and self.ballpos[1] <= self.platformpos_up[3]:
        ballpos_x = (self.ballpos[0]+self.ballpos[2])/2
        if self.ballpos[2] >= self.platformpos_up[0] and self.ballpos[0] <= self.platformpos_up[2]:
            if self.ballpos[1] <= self.platformpos_up[3]:
                self.ball_move_x = (np.random.random() * 2) - 1
                self.ball_move_y *= -1
                self.platform_up.state = 'atk'
                self.platform_down.state = 'def'
                self.reward += (1 + self.combo * 0.1)
                self.combo += 1;print(f'ballpos:{self.ballpos},platformpos:{self.platformpos_up}')

        # if self.ballpos[2] >= self.platformpos_down[0] and self.ballpos[0] <= self.platformpos_down[2]:
        #     if self.ballpos[3] >= self.platformpos_down[1] and self.ballpos[1] <= self.platformpos_down[3]:
        if self.ballpos[2] >= self.platformpos_down[0] and self.ballpos[0] <= self.platformpos_down[2]:
            if self.ballpos[3] >= self.platformpos_down[1]:
                self.platform_up.state = 'def'
                self.platform_down.state = 'atk'
                self.ball_move_x = (np.random.random() * 2) - 1
                self.ball_move_y *= -1
                self.reward += (1 + self.combo * 0.1)
                self.combo += 1;print(f'ballpos:{self.ballpos},platformpos:{self.platformpos_down}')




    def get_obs(self,ballpos,pos):
        ballposx = (ballpos[0]+ballpos[2])/2
        ballposy = (ballpos[1]+ballpos[3])/2
        posx = (pos[0] + pos[2]) / 2
        posy = (pos[1] + pos[3]) / 2
        dis = np.linalg.norm(np.array([ballposx,ballposy])-np.array([posx,posy]))

        atk = 1 if self.platform_up.state=='atk' else 0

        return np.array([posx,posy,ballposx,ballposy,dis,atk])
    def reset(self):
        self.canvas.delete(self.ball.id)
        m=Middleline(self.canvas,self.window_W,self.window_H)
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
        self.testtime += 1 ;print('testtime:',self.testtime)
        avg=np.mean(self.rewardlst)
        self.avgreward.append(avg);print(f'avg reward:{avg}')
        self.rewardlst = []
        try:
            self.combolst.append(self.combo) ;print('combo:',self.combo)

        except:
            pass
        self.combo = 0
        print(self.atk)
        if self.atk=='up':
            obs = self.get_obs(self.ballpos,self.platformpos_down)
        elif self.atk=='down':
            obs = self.get_obs(self.ballpos,self.platformpos_up)
        return obs

    def render(self, mode='human', clode=False):
        pass

    def close(self):
        self.tk.destroy()


if __name__=='__main__':
    g=Bouncy_ballv2()