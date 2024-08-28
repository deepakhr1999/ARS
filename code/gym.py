from omnisafe.envs import make as old_make
import torch

class Spec:
    timestep_limit:int = 1000

class BackwardsWrapper:
    def __init__(self, env):
        self._env = env
        self.steps = 0
        self.spec = Spec()

    def step(self, action):
        self.steps += 1
        obs, reward, cost, terminated, truncated, info  = self._env.step(torch.FloatTensor(action))
        return obs.numpy(), reward.item(), (terminated.item() or truncated.item() or self.steps >= self.spec.timestep_limit), info

    def reset(self):
        self.steps = 0
        return self._env.reset()[0].numpy()

    @property
    def observation_space(self):
        return self._env.observation_space
    
    @property
    def action_space(self):
        return self._env.action_space
    
    def seed(self, seed: int):
        self._env.set_seed(seed)

def make(env_id):
    print("Gottem!")
    return BackwardsWrapper(old_make(env_id))
