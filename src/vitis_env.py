import tcl
import stable_baselines3
import gym
from gym import spaces
from directives import Directive


class VitisEnv(gym.Env):
    def __init__(self, directive_file: str) -> None:
        self.tcl = tcl.Tcl(directive_file, read_only=False)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode):
        pass


env = VitisEnv("./directives.tcl")
print(env.tcl.loop_count)