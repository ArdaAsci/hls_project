from csynth import Csynth
import tcl
import stable_baselines3
import gym
from gym import spaces
from directives import Directive


class HlsEnv(gym.Env):
    def __init__(
        self,
        project_dir: str,
        project_name: str,
        solution_name: str,
        top_name: str,
        initial_directive_file: str,
    ) -> None:
        self.tcl = tcl.Tcl(initial_directive_file, read_only=True)
        csynth_file = project_dir + project_name + "/" + solution_name + "/syn/report/csynth.xml"
        self.csynth = Csynth(csynth_file)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode):
        pass


env = HlsEnv(project_dir="D:/vivado/vitis_rl/",
             project_name="matrixmul_prj",
             solution_name="solution1",
             top_name="matrixmul",
             initial_directive_file="./directives.tcl")