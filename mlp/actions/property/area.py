from random import shuffle
from .property import Property
from ...grid import HexGrid
from ...tools import dotdict
from ...replication_manager import MetaRegistry

AREAS = MetaRegistry()['Area']
AreaMeta = MetaRegistry().make_registered_metaclass("Area")


class Area(Property, metaclass=AreaMeta):

    _grid = None

    def get(self, context):
        pass

    @property
    def grid(self):
        if not self._grid:
            self._grid = HexGrid.locate()
        return self._grid


class Cell(Area):

    def __init__(self, cell):
        self.cell = cell

    def get(self, context):
        return [self.cell.get(context)]


class Adjacent(Area):

    def __init__(self, center):
        self.center = center

    def get(self, context):
        center = self.center.get(context)
        return center.adjacent


class Melee(Area):

    def __init__(self, radius, center):
        self.radius = radius
        self.center = center

    def get(self, context):
        grid = self.grid
        for cell in grid.get_area(self.center.get(context), self.radius):
            if cell.object and cell.object.stats.owner != context['owner'].stats.owner:
                return [cell]
        return []


class Line(Area):

    def __init__(self, source, target, length):
        self.source = source
        self.target = target
        self.length = length

    def get(self, context):
        grid = self.grid
        return grid.get_line(self.source.get(context), self.target.get(context), self.length)


class KNearestNeighbors(Area):

    def __init__(self, source, area, k, filter):
        self.source = source
        self.area = area
        self.k = k
        self.filter = filter

    def get(self, context):
        grid = self.grid
        area = self.area.get(context)
        filter_ = self.filter
        source = self.source.get(context)
        d_pairs = [
            (grid.distance(cell, source), cell) for cell in area if filter_.get(dotdict({'object': cell.object}))
        ]
        return [pair[-1] for pair in sorted(d_pairs, reverse=True)[:self.k:]]


class KRandomCells(Area):

    def __init__(self, area, k, filter):
        self.area = area
        self.filter = filter
        self.k = k

    def get(self, context):
        cells = self.area.get(context)
        filter_ = self.filter
        actual_cells = [cell for cell in cells if filter_.get(dotdict({'cell': cell}))]
        shuffle(actual_cells)
        return actual_cells[:self.k:]


class Circle(Area):

    def __init__(self, center, r):
        self.center = center
        self.r = r

    def get(self, context):
        return self.grid.get_area(self.center.get(context), self.r)

# AREAS = {
#     "Melee": Melee,
#     "Line": Line,
#     "KNearestNeighbors": KNearestNeighbors,
#     "Circle": Circle,
# }


def area_constructor(loader, node):
    a_s = loader.construct_mapping(node)
    name = a_s.pop("name")
    area = AREAS[name](**a_s)
    return area

AREA_TAG = "!area"
