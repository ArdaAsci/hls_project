from typing import Any, List


class Loop:

    def __init__(self, name, iteration_count: int = 5, parent_loop = None) -> None:
        self.name = name
        self.iteration_count = iteration_count
        self.parent_loop: Loop = parent_loop
        self.child_loops: List[Loop] = []

    def add_child(self, child):
        self.child_loops.append(child)

    def set_parent(self, parent):
        self.parent_loop = parent

    @property
    def rank(self):
        rank = 0
        parent = self.parent_loop
        while parent is not None:
            rank += 1
            parent = parent.parent_loop
        return rank