from typing import List, Union

import numpy as np

from src.directives import (
    BasicDirective,
    Directive,
    LoopDirective,
    PipelineDirective,
    UnrollDirective,
)


######################################
class Tcl:
    def __init__(
        self,
        initial_directives: str,
        top_name: str,
        read_only=True,
        dirfile_name="./new_directives.tcl",
    ) -> None:
        """
        A class that handles all operations with the .tcl file provided
        
        :param initial_directives: The name of the tcl file with the initial directives
        :param read_only: Specify if the given tcl file should be modified or not.
        If true, a new file with the name `dirfile_name` will be created.

        """
        self.directives: List[Directive] = []
        self.read_only = read_only
        self.top_name = top_name
        initial_dirfile = open(initial_directives)
        for directive_line in initial_dirfile:
            self.add_directive_from_file(directive_line)
        if read_only:
            initial_dirfile.close()
            self.dirfile = open(dirfile_name, "w")
            self.dirfile_name = dirfile_name
        else:
            self.dirfile = initial_dirfile
            self.dirfile_name = initial_directives

    def initialize_loop_directives(self, loop_name):
        self.add_directive_from_file()

    def get_loop_pragma(self, loop_name: str):
        """
        Returns both the pragmas of a loop.
        """
        return np.array(
            [
                self.get_loop_parameter(loop_name, "unroll"),
                self.get_loop_parameter(loop_name, "pipeline"),
            ]
        )

    def set_loop_pragma(self, loop_name: str, pragma: np.ndarray):
        directive = self.__find_directive(loop_name)

    def get_loop_parameter(self, loop_name: str, directive_type: str):
        """
        Iterates through all the tracked directives to find the matching loop name
        If a loop_name match is found, returns the value of the directive's param.
        """
        directive = self.__find_directive(loop_name, directive_type)
        if directive is not None:  # found the directive we're looking for
            return directive.param
        return None

    def set_loop_parameter(self, loop_name: str, directive_type: str, val: int):
        """
        Iterates through all the tracked directives to find the matching loop name
        If a loop_name match is found, sets the value of the directive's param to val.

        TODO: Refactoring required - quite sloppy 
        """
        directive = self.__find_directive(loop_name, directive_type)
        if directive is not None:  # found the directive we're looking for
            directive.param = val
            return True
        return False

    def increment_loop_parameter(
        self, loop_name: str, directive_type: str, increment_by: int
    ):
        """
        For adding to the current value of the 
        """
        directive = self.__find_directive(loop_name, directive_type)
        directive.param += increment_by

    def __find_directives(self, loop_name: str, create=True):
        """
        Finds both directives with the specified loop name.
        """
        unroll_directive = self.__find_directive(loop_name, "unroll")
        pipeline_directive = self.__find_directive(loop_name, "pipeline")
        return (unroll_directive, pipeline_directive)

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
            if directive.loop_name != '"' + self.top_name + "/" + loop_name + '"':
                continue
            return directive
        return None  # loop_name - directive combo not found

    def add_directive_from_file(self, lines: Union[str, List[str]]):
        if lines is not list:
            lines = [lines]  # Convert "line" to a list if not already one
        for line in lines:
            line = line.rstrip()
            split = line.split()
            first = split[0]
            rest = split[1:]

            if first == "set_directive_pipeline":
                ii_val_idx = int(rest.index("-II")) + 1
                ii_val = int(rest[ii_val_idx])
                loop_name = rest[ii_val_idx + 1]
                others = rest[ii_val_idx + 2 :]
                new_direc = PipelineDirective(
                    loop_name=loop_name, ii=ii_val, others=others
                )

            elif first == "set_directive_unroll":
                factor_val_idx = int(rest.index("-factor")) + 1
                factor_val = int(rest[factor_val_idx])
                loop_name = rest[factor_val_idx + 1]
                others = rest[factor_val_idx + 2 :]
                new_direc = UnrollDirective(
                    loop_name=loop_name, factor=factor_val, others=others
                )
            else:
                new_direc = BasicDirective(line=line)
            self.directives.append(new_direc)

    @property
    def loop_count(self):
        """
        Iterates through all the directives to find all the unique loop names and returns the # of them.
        """
        loopnames = []
        for directive in self.directives:
            if isinstance(directive, LoopDirective):
                loopnames.append(directive.loop_name)
        return len(set(loopnames))

    def __str__(self) -> str:
        return str(self.directives)

    def file_str(self) -> str:
        """
        Create a .tcl formatted directives list as a string.
        """
        file_str = ""
        for directive in self.directives:
            file_str += directive.print() + "\n"
        return file_str

    def update_directives_file(self):
        """
        Flush the old directives and write the new ones with the updated parameters.
        Must be done before any hls cli call.
        """
        text = self.file_str()
        if not self.dirfile.writable:
            return False
        open(self.dirfile_name, "w").close()  # Flush the file
        self.dirfile.write(text)
        return True

    @property
    def current_directives_file(self):
        return self.dirfile_name
