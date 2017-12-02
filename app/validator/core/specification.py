from pygraph.classes.digraph import digraph
from typing import List


class MapSpecification:
    def __init__(self, graph: digraph, max_x: int, max_y: int):
        self._graph = graph
        self._max_x = max_x
        self._max_y = max_y

    @property
    def graph(self):
        return self._graph

    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y


class OrderSpecification:
    def __init__(self, start: (int, int), finish: (int, int)):
        self._start = start
        self._finish = finish

    @property
    def start(self):
        return self._start

    @property
    def finish(self):
        return self._finish


class TagsSpecification:
    def __init__(self, tags: List[int]):
        self._tags = tags

    @property
    def tags(self) -> List[int]:
        return self._tags


class LogSpecification:
    def __init__(self, states: List):
        self._states = states

    @property
    def states(self):
        return self._states
