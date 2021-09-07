from typing import Type
from directives import ExecuteDirective, directive
import os

class Tcl():
    
    def __init__(self) -> None:
        self.directives = []

    def add_directive(self, line: str):
        split = line.split()
        first = split[0]
        rest = split[1:]
        if first == "open_project":
            opendir_obj = line.split()[1]
            self.directives.append(
                directive("open", "project", opendir_obj))
        elif first == "open_solution":
            opendir_obj = line.split()[1]
            self.directives.append(
                directive("open", "solution", opendir_obj))
        elif first == "set_directive_top":
            setting = ""
            setting.join(rest)
            self.directives.append(directive("set", "top", setting))
        elif first == "set_directive_pipeline":
            setting = ""
            setting.join(rest)
            self.directives.append(directive("set", "pipeline", setting))
        if rest == []:
            self.directives.append(directive("execute", first))

    def prnt(self):
        print(self.directives)