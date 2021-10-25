from typing import Any, List


class Loop:
    """
    A Class structure to represent a Loop in the C code.
    If nested, it has a reference to its parent loop a list of child loops.
    """

    def __init__(
        self, name, iteration_count: int = 5, parent_loop=None, rank=0
    ) -> None:
        self.name = name
        self.iteration_count = iteration_count
        self.parent_loop: Loop = parent_loop
        if self.parent_loop == None:
            self.rank = rank
        else:
            self.rank = self.parent_loop.rank
        self.child_loops: List[Loop] = []

    def add_child(self, child):
        self.child_loops.append(child)

    def set_parent(self, parent):
        self.parent_loop = parent

    def remove_all_children(self):
        self.child_loops: List[Loop] = []

    def remove_child(self, child_name: str):
        if child_name in self.child_loops:
            self.child_loops.remove(child_name)
            return True
        return False

    @property
    def nested_number(self):
        """
        Which layer this loop is in its nested loops.
        0 for top level
        """
        nested_number = 0
        parent = self.parent_loop
        while parent is not None:
            nested_number += 1
            parent = parent.parent_loop
        return nested_number

    @property
    def total_nested_depth(self):
        """
        How many layers there are in this loops nested loops.
        """
        if self.child_loops == []:
            return self.nested_number
        child_depth = [child.total_nested_depth for child in self.child_loops]
        return max(child_depth)
