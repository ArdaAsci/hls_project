from typing import List, Type, Union
from directives import BasicDirective, Directive, LoopDirective, PipelineDirective, UnrollDirective


class Tcl():
    def __init__(self,
                 initial_directives: str,
                 top_name: str,
                 read_only=False,
                 dirfile_name="./new_directives.tcl") -> None:
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
            self.add_directive(directive_line)
        if read_only:
            initial_dirfile.close()
            self.dirfile = open(dirfile_name, "w")
            self.dirfile_name = dirfile_name
        else:
            self.dirfile = initial_dirfile
            self.dirfile_name = initial_directives

    def set_loop_parameter(self, loop_name: str, directive_type: str,
                           val: int):
        """
        Iterates through all the tracked directives to find the matching loop name
        If a loop_name match is found, sets the value of the directives param to val.

        TODO: Refactoring required - quite sloppy 
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
            # found the directive we're looking for
            directive.param = val
            return

    def add_directive(self, lines: Union[str, List[str]]):
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
                others = rest[ii_val_idx + 2:]
                new_direc = PipelineDirective(loop_name=loop_name,
                                              ii=ii_val,
                                              others=others)

            elif first == "set_directive_unroll":
                factor_val_idx = int(rest.index("-factor")) + 1
                factor_val = int(rest[factor_val_idx])
                loop_name = rest[factor_val_idx + 1]
                others = rest[factor_val_idx + 2:]
                new_direc = UnrollDirective(loop_name=loop_name,
                                            factor=factor_val,
                                            others=others)
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

    @property
    def loop_names(self) -> List[str]:
        pass

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

    def update_directives(self):
        """
        Flush the old directives and write the new ones with the updated parameters
        """
        text = self.file_str()
        if not self.dirfile.writable:
            return False
        open(self.dirfile_name, "w").close()  # Flush the file
        self.dirfile.write(text)
        return True