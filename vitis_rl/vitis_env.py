import xml.etree.ElementTree
import stable_baselines3
import gym
from gym import spaces
from directive import Directive, OpenDirective, SetDirective, ExecuteDirective


class VitisEnv(gym.Env):

    def __init__(self, directives_file: str) -> None:
        self.dir_file = open(directives_file)
        self.directives = []
        dirs = []
        for directive in self.dir_file:
            dirs.append(directive)
        self.eval_directives(dirs)
        pass

    def eval_directives(self, dirs):
        for dir in dirs:
            print(dir)
            split = dir.split()
            first = split[0]
            rest = split[1:]
            if first == "open_project":
                opendir_obj = dir.split()[1]
                self.directives.append(OpenDirective("project", opendir_obj))
            elif first == "open_solution":
                opendir_obj = dir.split()[1]
                self.directives.append(OpenDirective("solution", opendir_obj))
            elif first == "set_directive_top":
                setting = ""
                setting.join(rest)
                self.directives.append(SetDirective("top", setting))
            elif first == "set_directive_pipeline":
                setting = ""
                setting.join(rest)
                self.directives.append(SetDirective("pipeline", setting))
            if rest == []:
                self.directives.append(ExecuteDirective(first))
        print(self.directives)

    def step(self, action):
        pass

    def reset(self):
        pass



if __name__ == "__main__":
    env = VitisEnv("./directives.tcl")