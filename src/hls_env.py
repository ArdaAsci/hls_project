import os
from typing import List

from gym import spaces, Env

from src.constants import ACTION_SPACE_SIZE
from src.csynth import Csynth
from src.directives import Directive
from src.loops import Loop
from src.tcl_reader import Tcl


class HlsEnv(Env):
    """
    An rl environment that also handles the high level operation of the Csynth and Tcl modules.
    TODO: Implement support for multiple projects-solutions
    """

    def __init__(
        self,
        project_dir: str,
        project_name: str,
        solution_name: str,
        top_name: str,
        initial_directive_file_name: str,
        loop_list: List[Loop],
    ) -> None:

        self.tcl = Tcl(initial_directive_file_name, top_name=top_name, read_only=True)

        self.csynth = Csynth(
            file_name=self.csynth_file_path(project_dir, project_name, solution_name)
        )

        self.action_space = spaces.Discrete(
            ACTION_SPACE_SIZE
        )  # Each loop requires 3 discrete actions
        self.observation_space = spaces.Dict(
            {
                "rank": spaces.Box(low=1, high=100, shape=(1,)),
                "total_loops": spaces.Box(low=1, high=100, shape=(1,)),
                "curr_nested_number": spaces.Box(low=1, high=100, shape=(1,)),
                "nested_number": spaces.Box(low=1, high=100, shape=(1,)),
                "loop_iter_count": spaces.Box(low=1, high=100, shape=(1,)),
                "curr_latency": spaces.Box(low=1, high=1000, shape=(1,)),
                "utilization": spaces.Box(low=0, high=1, shape=(1,)),
                "curr_pragma": spaces.Box(low=1, high=100, shape=(1,)),
            }
        )
        self.current_loop_index = 0
        self.current_pragma_type = False  # False for pipeline / True for unroll
        self.loop_list = loop_list
        self.top_module_data = self.csynth.top_module_data

    def step(self, action):
        current_loop = self.current_loop
        current_pragma_name = "unroll" if self.current_pragma_type else "pipeline"
        action += -1  # map actions [0 1 2] -> [-1 0 1]
        self.tcl.increment_loop_parameter(current_loop.name, current_pragma_name, -1)
        self.tcl.update_directives_file()
        self.run_vitis_with_directive(self.tcl.current_directives_file)
        done = self.next_pragma()
        new_current_loop = self.current_loop
        observation = self.get_observation(new_current_loop)
        reward = self.calc_reward(observation["utilization"])
        info = {}
        return observation, reward, done, info

    def reset(self):
        self.current_loop_index = 0
        self.current_pragma_type = False
        current_loop = self.current_loop
        observation = self.get_observation(current_loop)
        return observation

    def get_observation(self, current_loop: Loop):
        observation = {
            "rank": current_loop.rank,
            "total_loops": len(self.loop_list),
            "curr_nested_number": current_loop.nested_number,
            "nested_number": current_loop.total_nested_depth,
            "loop_iter_count": current_loop.iteration_count,
            "curr_latency": self.top_module_data.latency,
            "utilization": self.calc_utilization(),
            "curr_pragma": 0 if self.current_pragma_type else 1,
        }
        return observation

    def calc_utilization(self):
        total_used_area_ratios = self.top_module_data.used_area_ratio
        ratios_list = list(total_used_area_ratios.values())
        ratios_list = [ratio for ratio in ratios_list if ratio is not None]
        return sum(ratios_list) / len(ratios_list)

    def calc_reward(self, utilization: float, latency: float):
        return NotImplementedError()

    @property
    def current_loop(self):
        return self.loop_list[self.current_loop_index]

    @property
    def current_pragma(self):
        return "unroll" if self.current_pragma_type else "pipeline"

    def next_pragma(self):
        """
        Switches to the next pragma by changing the loop index and/or pragma type
        returns true if this is the last pragma.
        """
        if not self.current_pragma_type:
            self.current_pragma_type = True
        else:
            self.current_pragma_type = False
            self.current_loop_index += 1
        if (
            self.current_loop_index + 1 == len(self.loop_list)
            and self.current_pragma_type
        ):
            return True
        return False

    @staticmethod
    def run_vitis_with_directive(directive_file):
        os.popen(os.popen("vitis_hls -f " + directive_file))

    @staticmethod
    def csynth_file_path(project_dir: str, project_name: str, solution_name: str):
        """
        Generates the full path of the Csynth file from the given (project directory, project name, solution name)
        """
        return (
            project_dir
            + "/"
            + project_name
            + "/"
            + solution_name
            + "/syn/report/csynth.xml"
        )

    @property
    def empty_observation(self):
        return {
            "rank": 0,
            "total_loops": 0,
            "curr_nested_number": 0,
            "nested_number": 0,
            "loop_iter_count": 0,
            "curr_latency": 0,
            "utilization": 0,
            "curr_pragma": 0,
        }

    def render(self, mode):
        pass
