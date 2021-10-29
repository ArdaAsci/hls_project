from typing import List, Union

import numpy as np

from src.directives import (
    BasicDirective,
    Directive,
    LoopDirective,
    PipelineDirective,
    UnrollDirective,
)


class Tcl2:

    insert_idx = 3

    def __init__(
        self,
        project_name: str,
        top_name: str,
        solution_name: str,
        directives_file_name: str = "directives.tcl",
    ) -> None:
        """
        The 2.0 version of the Tcl class. Previously, the objective was to read the
        given .tcl file for the parameters and update them later.
        In this version, we create a barebone tcl file and populate it with pragmas 
        by external function calls.
        """
        self.directives: list[Directive] = []
        self.project_name = project_name
        self.top_name = top_name
        self.solution_name = solution_name
        self.tcl_file_fullpath = "./" + project_name + "/" + directives_file_name
        self.reset_tcl()

    def set_loop_pragmas(self, loop_names: Union[str, list[str]], val: np.ndarray):
        """
        Set the pragmas for the given loop names
        """
        if isinstance(loop_names, str):
            loop_names = [loop_names]
        idx = 0
        for loop_name in loop_names:
            unroll, pipeline = self.__find_directives(loop_name)
            unroll.param = val[idx * 2]
            pipeline.param = val[idx * 2 + 1]
            idx += 1

    def add_loop_pragmas(self, loop_names: Union[str, list[str]], val: np.ndarray):
        """
        For creating both the pragmas of a list of loops (or single loop)
        """
        if isinstance(loop_names, str):
            loop_names = [loop_names]
        idx = 0
        for loop_name in loop_names:
            self.__add_loop_pragma(loop_name, "pipeline", int(val[idx * 2 + 1]))
            self.__add_loop_pragma(loop_name, "unroll", int(val[idx * 2]))
            idx += 1

    def __add_loop_pragma(self, loop_name: str, directive_type: str, val: int):
        """
        For creating a pragma for the specified loop_name, directive type and initial value.
        """
        if directive_type == "unroll":
            self.directives.insert(
                Tcl2.insert_idx, UnrollDirective(self.top_name + "/" + loop_name, val)
            )
        elif directive_type == "pipeline":
            self.directives.insert(
                Tcl2.insert_idx, PipelineDirective(self.top_name + "/" + loop_name, val)
            )

    def __find_directives(self, loop_name: str):
        unroll = self.__find_directive(loop_name, "unroll")
        pipeline = self.__find_directive(loop_name, "pipeline")
        return (unroll, pipeline)

    def __find_directive(self, loop_name: str, directive_type: str):
        """
        Finds the directive with the specified loop name and directive
        Returns None if not found
        """
        directive_class = LoopDirective
        if directive_type == "unroll":
            directive_class = UnrollDirective
        elif directive_type == "pipeline":
            directive_class = PipelineDirective
        for directive in self.directives:
            if not isinstance(directive, directive_class):
                continue
            if directive.loop_name != self.top_name + "/" + loop_name:
                continue
            return directive
        return None  # loop_name - directive combo not found

    def reset_tcl(self):
        """
        Clears all the pragmas from the directives file.
        """
        self.directives = []
        self.directives.append(BasicDirective(f"open_project {self.project_name}"))
        self.directives.append(BasicDirective(f"open_solution {self.solution_name}"))
        self.directives.append(
            BasicDirective(f'set_directive_top -name {self.top_name} "{self.top_name}"')
        )
        self.directives.append(BasicDirective("csim_design"))
        self.directives.append(BasicDirective("csynth_design"))
        self.directives.append(BasicDirective("cosim_design"))
        self.directives.append(BasicDirective("exit"))
        self.update_directives_file()

    def update_directives_file(self):
        """
        Flush the old directives and write the new ones with the updated parameters.
        Must be done before any hls cli call.
        """
        text = self.__file_str()
        file_handle = open(self.tcl_file_fullpath, "w")
        file_handle.write(text)
        file_handle.close()

    def __file_str(self) -> str:
        """
        Create a .tcl formatted directives list as a string.
        """
        file_str = ""
        for directive in self.directives:
            file_str += directive.print() + "\n"
        return file_str

    @property
    def directive_file_path(self):
        return self.tcl_file_fullpath

