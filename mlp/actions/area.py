class Area:

    def get(self, action):
        pass


class Melee(Area):

    def __init__(self, radius, center):
        self.radius = radius
        self.center = center

    def get(self, action):
        grid = action.owner.cell.grid
        for cell in action.owner.cell.grid.get_area(self.center.get(action), self.radius):
            if cell.object and cell.object.stats.owner != action.owner.stats.owner:
                return [cell]
        return []

AREAS = {
    "Melee": Melee
}
