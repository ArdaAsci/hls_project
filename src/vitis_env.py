from tcl_read import Tcl
import xml.etree.ElementTree
import stable_baselines3
import gym
from gym import spaces
from directives import Directive, OpenDirective, SetDirective, ExecuteDirective, directive


class VitisEnv(gym.Env):
    def __init__(self, directives_file: str) -> None:
        self.dir_file = open(directives_file)
        self.tcl = Tcl()
        for directive in self.dir_file:
            self.tcl.add_directive(directive)            
        self.tcl.prnt()

    def step(self, action):
        pass

    def reset(self):
        pass


env = VitisEnv("./directives.tcl")
print("what")