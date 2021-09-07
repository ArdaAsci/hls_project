from abc import ABC
from dataclasses import dataclass
from typing import List


@dataclass
class Directive(ABC):
    pass


@dataclass
class OpenDirective(Directive):
    open_type: str
    obj: str
    pass


@dataclass
class SetDirective(Directive):
    set_type: str
    settings: str
    pass


@dataclass
class ExecuteDirective(Directive):
    exe_type: str
    pass
