from typing import Any, List


class Loop:
    """
    A Class structure to represent a Loop in the C code.
    If nested, it has a reference to its parent loop a list of child loops.
    """

    def __init__(self, name, iteration_count: int = 5, parent_loop=None) -> None:
        self.name = name
        self.iteration_count = iteration_count
        self.parent_loop: Loop = parent_loop
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
    def rank(self):
        rank = 0
        parent = self.parent_loop
        while parent is not None:
            rank += 1
            parent = parent.parent_loop
        return rank
