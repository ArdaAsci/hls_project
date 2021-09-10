from typing import List
from loops import Loop
from csynth import Csynth
from tcl_reader import Tcl
import stable_baselines3
import gym
from gym import spaces
from directives import Directive


class HlsEnv(gym.Env):
    def __init__(self, project_dir: str, project_name: str, solution_name: str,
                 top_name: str, initial_directive_file: str,
                 loop_list: List[Loop]) -> None:
        self.tcl = Tcl(initial_directive_file,
                       top_name=top_name,
                       read_only=True)
        csynth_file = project_dir + project_name + "/" + solution_name + "/syn/report/csynth.xml"
        self.csynth = Csynth(csynth_file)

        self.action_space = spaces.MultiDiscrete([
            3 for i in range(len(loop_list))
        ])  # Each loop requires 3 discrete actions

        self.observation_space = spaces.Dict({
            "rank":
            spaces.Box(low=1, high=100, shape=(1, )),
            "#loops":
            spaces.Box(low=1, high=100, shape=(1, )),
            "curr_nested_number":
            spaces.Box(low=1, high=100, shape=(1, )),
            "nested_number":
            spaces.Box(low=1, high=100, shape=(1, )),
            "loop_iter_count":
            spaces.Box(low=1, high=100, shape=(1, )),
            "curr_latency":
            spaces.Box(low=1, high=1000, shape=(1, )),
            "utilization":
            spaces.Box(low=0, high=1, shape=(5, )),
            "curr_pragma":
            spaces.Box(low=1, high=100, shape=(2, ))
        })

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode):
        pass
