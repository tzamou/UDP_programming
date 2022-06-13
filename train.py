import gym
import matplotlib.pyplot as plt
from stable_baselines3 import DQN
from sb3_contrib.qrdqn import QRDQN

class Algorithm:
    def __init__(self,envid="BouncyBall-v2",timesteps=1000_0000,model_name="./model/qrdqn_BouncyBallv2-n"):
        self.env = gym.make(envid)
        self.timesteps = timesteps
        self.model_name = model_name
        self.model = None
    def train(self,loadmodel=None,verbose=1):
        """
        :param loadmodel: "./model/qrdqn_BouncyBallv2"
        :param verbose: 1
        :return:
        """
        if loadmodel == None:
            self.model = QRDQN("MlpPolicy", self.env, verbose=verbose)
        else:
            self.model = QRDQN.load(loadmodel, env=self.env)
        self.model.learn(total_timesteps=self.timesteps, log_interval=4)
        self.model.save(self.model_name)
        plt.plot(self.env.avgreward)
        plt.title('QRDQN v2-1')
        plt.show()
        plt.gca()
        plt.title('combo v2-1')
        plt.plot(self.env.combolst)
        plt.show()
        del self.model
        self.env.close()
    def predict(self,model_name="./model/qrdqn_BouncyBallv2"):
        model = QRDQN.load(model_name)
        obs = self.env.reset()
        for i in range(100000):
            # while True:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = self.env.step(action)
            self.env.render()
            if done:
                obs = self.env.reset()

if __name__=='__main__':
    algo=Algorithm()
    algo.train()
    algo.predict()
