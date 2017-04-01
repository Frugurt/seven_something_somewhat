from .property import Property


class Area(Property):

    def get(self, action):
        pass


class Melee(Area):

    def __init__(self, radius, center):
        self.radius = radius
        self.center = center

    def get(self, action):
        grid = action.owner.cell.grid
        for cell in grid.get_area(self.center.get(action), self.radius):
            if cell.object and cell.object.stats.owner != action.owner.stats.owner:
                return [cell]
        return []


class Line(Area):

    def __init__(self, source, target, length):
        self.source = source
        self.target = target
        self.length = length

    def get(self, action):
        grid = action.owner.cell.grid
        return grid.get_line(self.source.get(action), self.target.get(action)[-1], self.length)


AREAS = {
    "Melee": Melee,
    "Line": Line,
}


def area_constructor(loader, node):
    a_s = loader.construct_mapping(node)
    name = a_s.pop("name")
    area = AREAS[name](**a_s)
    return area

AREA_TAG = "!area"
