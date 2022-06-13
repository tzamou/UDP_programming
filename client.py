import socket
import threading, pygame
from src import BouncyBall_Game,Login
from sb3_contrib.qrdqn import QRDQN


class Client:
    def __init__(self):
        self.sck = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.data = str()
    def receve(self):
        while True:
            self.sck.sendto(self.data.encode('utf-8'),('127.0.0.1',5000))
            data2, addr = self.sck.recvfrom(1024)
            self.act=data2.decode('utf-8')
            if self.act != '':
                print('data:',self.act)
        self.sck.close()


if __name__=="__main__":
    c = Client()
    td=threading.Thread(target=c.receve)
    td.setDaemon(True)
    td.start()
    game=Login()
    while True:
        c.data = game.message
        try:
            game.keyinput()
        except Exception as e:
            print(e)
        if c.act=='Start':
            break
    model = QRDQN.load("./model/qrdqn_BouncyBallv2")
    env = BouncyBall_Game()
    obs = env.reset()
    mode='Manual'
    pygame.mixer.init()
    pygame.mixer.music.load('./bgm.mp3')
    pygame.mixer.music.play(-1)
    play=1
    while True:
        action, _states = model.predict(obs, deterministic=True)
        if c.act=='Auto':
            mode='Auto'
        elif c.act=='Manual':
            mode='Manual'
        if mode=='Manual':
            obs, reward, done, info = env.step(action, playing=True, act=c.act)
        elif mode=='Auto':
            obs, reward, done, info = env.step(action, playing=False)
        if c.act=='Music':
            if play==1:
                play=0
                pygame.mixer.music.stop()
            elif play==0:
                play=1
                pygame.mixer.music.play(-1)
        c.data = env.message
        if done:
            obs = env.reset()






