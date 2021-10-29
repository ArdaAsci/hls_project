from __future__ import annotations
from typing import Any, Iterator, List, Union
import numpy as np
from numpy.lib.function_base import iterable


class LoopList:
    """
    A list wrapper for storing all the Loop instances of a project.
    """

    def __init__(self, *loops: Loop) -> None:
        self.loops = list(loops)

    @property
    def loop_names(self) -> list[str]:
        return [loop.name for loop in self.loops]

    @property
    def full_pragma(self) -> np.ndarray:
        return np.concatenate([loop.pragma for loop in self.loops])

    def __len__(self):
        return len(self.loops)

    def __getitem__(self, idx) -> Loop:
        return self.loops[idx]

    def __iter__(self):
        return iter(self.loops)

    def get_pragma(self, index):
        return self.loops[index].pragma

    def get_loop(self, loop_name: str):
        return self.loops[self.__find_loop_index_name(loop_name)]

    def __find_loop_index_ref(self, loop: Loop):
        if loop in self.loops:
            return self.loops.index(loop)
        raise ValueError("Given loop could not be found.")

    def __find_loop_index_name(self, name: str):
        if name in self.loop_names:
            return self.loop_names.index(name)
        raise ValueError("Given loop name could not be found.")


class Loop:
    """
    A Class structure to represent a Loop in the C code.
    If nested, it has a reference to its parent loop a list of child loops.
    """

    def __init__(
        self,
        name,
        iteration_count: int = 5,
        parent_loop: Loop = None,
        pragma: np.ndarray = np.zeros(2),
        rank=0,
    ) -> None:
        self.name = name
        self.iteration_count = iteration_count
        self.__pragma = pragma
        self.child_loops: list[Loop] = []

        if parent_loop is None:
            self.rank = rank
            self.parent_loop = None
        else:
            self.rank = parent_loop.rank
            self.set_parent(parent_loop)

    @property
    def pragma(self) -> np.ndarray:
        return self.__pragma

    @pragma.setter
    def pragma(self, val: np.ndarray) -> None:
        self.__pragma = val

    def increment_pragma(self, delta: np.ndarray):
        self.__pragma += delta

    def add_child(self, child: Loop):
        if child not in self.child_loops:
            self.child_loops.append(child)
        else:
            raise ValueError("Given loop is already in the child_loops")

    def set_parent(self, parent: Loop):
        self.parent_loop = parent
        self.parent_loop.add_child(self)

    def remove_all_children(self):
        """
        For removing all references in the child_loops list.
        """
        self.child_loops: List[Loop] = []

    def remove_child(self, child: Union[Loop, str]):
        """
        For removing a Loop reference from the child_loops list.
        """
        if isinstance(child, Loop):
            return self.__remove_child_by_loop(child_loop=child)
        elif isinstance(child, str):
            return self.__remove_child_by_name(child_name=child)
        else:
            raise TypeError(
                "Remove Child only accepts Union[Loop, str] failed to remove child loop"
            )

    def __remove_child_by_name(self, child_name: str):
        child_names = [child.name for child in self.child_loops]
        if child_name in child_names:
            child_index = child_names.index(child_name)
            self.child_loops.pop(child_index)

        else:
            raise ValueError("Given loop name could not be found")
        return False

    def __remove_child_by_loop(self, child_loop: Loop):
        if child_loop in self.child_loops:
            self.child_loops.remove(child_loop)
        else:
            raise ValueError("Given loop object could not be found in child_loops")
        pass

    @property
    def nested_number(self):
        """
        Which layer this loop is in its nested loops.
        0 for top level
        """
        if self.parent_loop is None:
            return 0
        else:
            return self.parent_loop.nested_number + 1

    @property
    def total_nested_depth(self):
        """
        How many layers there are in this loops nested loops.
        """
        if self.child_loops == []:
            return self.nested_number
        child_depth = [child.total_nested_depth for child in self.child_loops]
        return max(child_depth)
