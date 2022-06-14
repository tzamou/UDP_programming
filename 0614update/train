import gym
import matplotlib.pyplot as plt
from sb3_contrib.qrdqn import QRDQN
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.logger import configure

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

        checkpoint_callback = CheckpointCallback(save_freq=200_0000, save_path='./model/check_log/',
                                                 name_prefix='QRDQN_model')

        ###
        tmp_path = "./sb3_log/"
        new_logger = configure(tmp_path, ["stdout", "csv"])
        self.model.set_logger(new_logger)
        ###
        self.model.learn(total_timesteps=self.timesteps, log_interval=4, callback=checkpoint_callback)
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
    algo=Algorithm(timesteps=2000_0000,model_name="./model/qrdqn_BouncyBallv2_0614")
    algo.train()
    #algo.predict()
