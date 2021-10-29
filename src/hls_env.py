import os

import numpy as np
from gym import Env, spaces

from src.constants import ACTION_SPACE_SIZE
from src.csynth import Csynth
from src.loops import Loop, LoopList
from src.tcl import Tcl2


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
        loop_list: LoopList,
    ) -> None:

        self.csynth = Csynth(
            file_name=self.csynth_file_path(project_dir, project_name, solution_name)
        )
        self.initial_module_data = self.csynth.top_module_data
        obs_space = {
            "rank": spaces.Box(low=1, high=100, shape=(1,)),
            "total_loops": spaces.Box(low=1, high=100, shape=(1,)),
            "curr_nested_number": spaces.Box(low=1, high=100, shape=(1,)),
            "nested_number": spaces.Box(low=1, high=100, shape=(1,)),
            "loop_iter_count": spaces.Box(low=1, high=100, shape=(1,)),
            "curr_latency": spaces.Box(low=1, high=1000, shape=(1,)),
            "utilization": spaces.Box(low=0, high=1, shape=(5,)),
            "curr_pragma": spaces.Box(low=0, high=100, shape=(len(loop_list) * 2,)),
        }
        boxes = list(obs_space.values())
        lows = [int(box.low[0]) for box in boxes]
        highs = [int(box.high[0]) for box in boxes]
        shapes = [int(box.shape[0]) for box in boxes]
        obs_low = np.repeat(lows, shapes)
        obs_high = np.repeat(highs, shapes)

        self.observation_space = spaces.Box(
            low=obs_low, high=obs_high, shape=(np.sum(shapes),),
        )
        self.action_space = spaces.MultiDiscrete(
            [ACTION_SPACE_SIZE, ACTION_SPACE_SIZE]
        )  # Each loop requires 3 discrete actions
        self.current_loop_index = 0
        self.loop_list = loop_list
        self.tcl = Tcl2(
            project_name=project_name, top_name=top_name, solution_name=solution_name
        )
        self.tcl.add_loop_pragmas(self.loop_list.loop_names, self.loop_list.full_pragma)

    def step(self, action: list[int]):
        current_loop = self.current_loop
        action_array = np.array(action)
        action_array += -1  # map actions [0 1 2] -> [-1 0 1]
        current_loop.increment_pragma(action_array)
        self.tcl.set_loop_pragmas(current_loop.name, current_loop.pragma)
        self.tcl.update_directives_file()
        self.run_vitis_with_directive(self.tcl.directive_file_path)
        self.csynth.update_modules(reconfigure_root=True)
        done = self.next_pragma()
        new_current_loop = self.current_loop
        observation = self.get_observation(new_current_loop)
        reward = self.calc_reward(self.csynth.top_module_data.latency)
        info = {}
        return observation, reward, done, info

    def reset(self):
        self.current_loop_index = 0
        observation = self.get_observation(self.current_loop)
        return observation

    def get_observation(self, current_loop: Loop):
        observation_dict = {
            "rank": np.array([current_loop.rank]),
            "total_loops": np.array([len(self.loop_list)]),
            "curr_nested_number": np.array([current_loop.nested_number]),
            "nested_number": np.array([current_loop.total_nested_depth]),
            "loop_iter_count": np.array([current_loop.iteration_count]),
            "curr_latency": np.array([self.csynth.top_module_data.latency]),
            "utilization": self.calc_utilization(),
            "curr_pragma": self.loop_list.full_pragma / self.observation_space.shape[0],
        }
        observation = np.concatenate(list(observation_dict.values()))
        return observation

    def calc_utilization(self) -> np.ndarray:
        total_used_area_ratios = self.csynth.top_module_data.used_area
        ratios_list = list(total_used_area_ratios.values())
        ratios_array = np.array([ratio for ratio in ratios_list if ratio is not None])
        initial_ratios = np.array(list(self.initial_module_data.used_area.values()))
        utilization = np.divide(
            ratios_array,
            initial_ratios,
            out=np.zeros_like(ratios_array, dtype=np.float64),
            where=initial_ratios != 0,
        )
        return utilization

    def calc_reward(self, latency: float):
        initial_latency = self.initial_module_data.latency
        return latency / initial_latency

    @property
    def current_loop(self):
        return self.loop_list[self.current_loop_index]

    def next_pragma(self):
        """
        Switches to the next pragma by changing the loop index and/or pragma type
        returns true if this is the last pragma.
        """
        self.current_loop_index += 1
        if self.current_loop_index + 1 == len(self.loop_list):
            return True
        return False

    @staticmethod
    def run_vitis_with_directive(directive_file):
        print(os.popen(f"vitis_hls -f {directive_file}").read())

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

    def render(self, mode):
        pass
