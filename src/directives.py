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

def directive(*args):
    first = args[0]
    rest = args[1:]
    if first == "open":
        return OpenDirective(*rest)
    elif first == "set":
        return SetDirective(*rest)
    elif first == "execute":
        return ExecuteDirective(*rest)
    else:
        return
