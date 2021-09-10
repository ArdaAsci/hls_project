from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Directive(ABC):
    r"""
    The superclass of all directive types.
    These classes are used for categorizing and tracking different
    directives in the "directives.tcl" file
    """
    @abstractmethod
    def print(self) -> str:
        r"""
        Get the .tcl file representation of a directive as an str
        """
        pass


@dataclass
class BasicDirective(Directive):
    r"""
    Any directive that does not need attention
    """
    line: str

    def print(self) -> str:
        return self.line


@dataclass
class ArrayDirective(Directive, ABC):
    array_name: str


@dataclass
class LoopDirective(Directive, ABC):
    loop_name: str
    param: int

    @param.setter
    def param(self, val):
        if self.check_set_validity():
            param = val

    @abstractmethod
    def check_set_validity(self, val):
        pass


@dataclass
class PipelineDirective(LoopDirective):
    others: List[str]

    def __init__(self, loop_name: str, ii: int, others: str = ""):
        assert ii >= 1, f"Pipeline ii ({ii}) must be >=1"
        super().__init__(loop_name=loop_name, param=ii)
        self.others = others

    def check_set_validity(self, val):
        return val >= 1

    def print(self) -> str:
        return "set_directive_pipeline -ii " + str(
            self.param) + " " + self.loop_name + " " + " ".join(self.others)


@dataclass
class UnrollDirective(LoopDirective):
    others: List[str]

    def __init__(self, loop_name: str, factor: int, others: str = ""):
        assert factor >= 0, f"Unrolling factor ({factor}) must be >=0"
        super().__init__(loop_name=loop_name, param=factor)
        self.others = others

    def check_set_validity(self, val):
        return val >= 0

    def print(self) -> str:
        return "set_directive_unroll -factor " + str(
            self.param) + " " + self.loop_name + " " + " ".join(self.others)
