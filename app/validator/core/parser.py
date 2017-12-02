from validator.core.specification import MapSpecification, OrderSpecification, LogSpecification, TagsSpecification
from pygraph.classes.digraph import digraph


class BaseParser:
    def __init__(self, path: str):
        with open(path, 'r') as file:
            self._parse(file)

    def _parse(self, file):
        raise NotImplementedError()

    @staticmethod
    def _parse_int(s: str) -> int:
        cleared_str = s.strip(" \n\r\t")
        if not cleared_str.isdigit():
            raise ValueError("Integer expected but arbitrary string received")

        return int(cleared_str)


class MapParser(BaseParser):
    def _parse(self, file):
        max_x = self._parse_int(file.readline())
        max_y = self._parse_int(file.readline())

        if max_x < max_y:
            raise ValueError("Map must be horizontal: max_x >= max_y")

        edge_count = self._parse_int(file.readline())

        graph = digraph()

        for i in range(0, (max_x + 1)*(max_y + 1)):
            graph.add_node(i)

        for _ in range(0, edge_count):
            edge = file.readline().split()

            if len(edge) != 4:
                raise ValueError("Edge must be represented by 4 numbers: x1 y1 x2 y2")

            x1 = self._parse_int(edge[0])
            y1 = self._parse_int(edge[1])
            x2 = self._parse_int(edge[2])
            y2 = self._parse_int(edge[3])

            graph.add_edge((y1*(max_x + 1) + x1, y2*(max_x + 1) + x2))

        self._specification = MapSpecification(graph, max_x, max_y)

    @property
    def specification(self) -> MapSpecification:
        return self._specification


class OrderParser(BaseParser):
    def _parse(self, file):
        route = file.readline().split()

        if len(route) != 4:
            raise ValueError("Order must contain only initial and final locations: x1 y1 x2 y2")

        x1 = self._parse_int(route[0])
        y1 = self._parse_int(route[1])
        x2 = self._parse_int(route[2])
        y2 = self._parse_int(route[3])

        self._specification = OrderSpecification((x1, y1), (x2, y2))

    @property
    def specification(self) -> OrderSpecification:
        return self._specification


class TagsParser(BaseParser):
    def _parse(self, file):
        tags = []
        for line in file:
            tags.append(self._parse_int(line))

        self._specification = TagsSpecification(tags)

    @property
    def specification(self) -> TagsSpecification:
        return self._specification


class LogParser(BaseParser):
    def __init__(self, path: str):
        super().__init__(path)

    def _parse(self, file):
        states = []
        var_count = None
        for line in file:
            state = line.split()

            if var_count is None:
                var_count = len(state)

            if len(state) != var_count:
                raise ValueError("Parsed number of variables is invalid: {} expected".format(str(var_count)))

            state = list(map(lambda v: self._parse_int(v), state))
            states.append(state)

        self._log_specification = LogSpecification(states)
        self._var_count = var_count

    @property
    def log_specification(self):
        return self._log_specification

    @property
    def var_count(self):
        return self._var_count


class PRISMResult(BaseParser):
    def _parse(self, file):
        lines = file.readlines()
        self._success = len(lines) == 2 and lines[0].strip() == "Result" and lines[1].strip() == "true"

    @property
    def success(self):
        return self._success