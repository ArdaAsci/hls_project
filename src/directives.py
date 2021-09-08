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
class LoopDirective(Directive, ABC):
    loop_name: str


@dataclass
class ArrayDirective(Directive, ABC):
    array_name: str


@dataclass
class PipelineDirective(LoopDirective):
    ii: int
    others: List[str]

    def __init__(self, loop_name: str, ii: int, others: str = ""):
        assert ii >= 1, f"Pipeline ii ({ii}) must be >=1"
        super().__init__(loop_name=loop_name)
        self.ii = ii
        self.others = others

    def set_ii(self, ii):
        assert ii >= 1, f"Pipeline ii ({ii}) must be >=1"
        self.ii = ii

    def print(self) -> str:
        return "set_directive_pipeline -ii " + str(
            self.ii) + " " + self.loop_name + " " + " ".join(self.others)


@dataclass
class UnrollDirective(LoopDirective):
    factor: int
    others: List[str]

    def __init__(self, loop_name: str, factor: int, others: str = ""):
        assert factor >= 0, f"Unrolling factor ({factor}) must be >=0"
        super().__init__(loop_name=loop_name)
        self.factor = factor
        self.others = others

    def set_factor(self, factor):
        assert factor >= 0, f"Unrolling factor ({factor}) must be >=0"
        self.factor = factor

    def print(self) -> str:
        return "set_directive_unroll -factor " + str(
            self.factor) + " " + self.loop_name + " " + " ".join(self.others)
