from itertools import (
    chain,
    product,
    permutations,
    repeat,
)
from operator import add, mul
from functools import (
    reduce,
)
from operator import add
from mlp.replication_manager import GameObject
from .tools import dict_merge


def sum_iterables(iter1, iter2):
    # print(iter1, iter2)
    return [add(*x) for x in zip(iter1, iter2)]


class Cell:

    hooks = ['take', 'place']

    def __init__(self, pos, grid=None, terrain=None):
        # super().__init__(id_=id_)
        self.grid = grid
        self.pos = pos
        self.adjacent = []
        self.additional_content = []
        self.object = None
        self.terrain = terrain or None

    def place(self, obj):
        self.object = obj
        # self.terrain = None

    def take(self, _):
        self.object = None

    def __repr__(self):
        return "{} at {}".format(self.__class__.__name__, self.pos)


class Grid(GameObject):

    hooks = []
    cell = Cell
    load_priority = 1

    def __init__(self, size=None, id_=None):
        super().__init__(id_)
        self.size = size
        self._grid = None
        if size is not None:
            self.create_cells()

    def create_cells(self):
        pass

    def get_ring(self, pos_or_cell, r):
        pass

    def get_area(self, pos_or_cell, r):
        pass

    def find_path(self, from_pos_or_cell, to_pos_or_cell):
        pass

    def make_cell(self, *args, **kwargs):
        return self.cell(*args, grid=self, **kwargs)

    def __getitem__(self, item):
        pass

    def load(self, struct):
        if self._grid is None:
            self.size = struct['size']
            self.create_cells()

    def dump(self):
        # return {
        #     **super().dump(),
        #     'size': self.size,
        # }
        return dict_merge(
            super().dump(),
            {'size': self.size}
        )


class RectCell(Cell):
    pass


class RectGrid(Grid):

    cell = RectCell

    def __init__(self, size=None, id_=None):
        super().__init__(id_)
        self.size = size
        self._grid = None
        if size is not None:
            self.create_cells()

    def create_cells(self):
        w, h = self.size
        self._grid = [[self.make_cell((i, j)) for j in range(h)] for i in range(w)]
        for i, j in product(range(w), range(h)):
            cur_cell = self._grid[i][j]
            if i > 0:
                cur_cell.adjacent.append(self._grid[i-1][j])
            if i < w - 1:
                cur_cell.adjacent.append(self._grid[i+1][j])
            if j > 0:
                cur_cell.adjacent.append(self._grid[i][j-1])
            if j < h - 1:
                cur_cell.adjacent.append(self._grid[i][j+1])

    def __getitem__(self, item):
        return self._grid[item[0]][item[1]]

    def __iter__(self):
        return iter(chain(*self._grid))


class HexCell(Cell):
    pass


class HexGrid(Grid):

    cell = HexCell

    def create_cells(self):
        w, h = self.size
        self._grid = [[self.make_cell((i, j)) for j in range(h)] for i in range(w)]
        for cell in self:
            coord = self.offsets_to_cube(cell.pos)
            for d in permutations([1, 0, -1]):
                adj_cell = self[sum_iterables(coord, d)]
                if adj_cell is not None:
                    cell.adjacent.append(adj_cell)
        # for i, j in product(range(w), range(h)):
        #     cur_cell = self._grid[i][j]
            # if i > 0:
            #     cur_cell.adjacent.append(self._grid[i - 1][j])
            # if i < w - 1:
            #     cur_cell.adjacent.append(self._grid[i + 1][j])
            # if j > 0:
            #     cur_cell.adjacent.append(self._grid[i][j - 1])
            # if j < h - 1:
            #     cur_cell.adjacent.append(self._grid[i][j + 1])

    @staticmethod
    def cube_to_offsets(pos):
        x, y, z = pos
        col = x
        row = z + (x + (x & 1)) // 2
        return col, row

    @staticmethod
    def offsets_to_cube(pos):
        col, row = pos
        x = col
        z = row - (col + (col & 1)) // 2
        y = -x - z
        return x, y, z

    def distance(self, cell_a, cell_b):
        pos_a = self.offsets_to_cube(cell_a.pos)
        pos_b = self.offsets_to_cube(cell_b.pos)
        return max((abs(a - b) for a, b in zip(pos_a, pos_b)))

    @staticmethod
    def inter(a, b, t):
        return a + (b - a)*t

    def cube_inter(self, pos_a, pos_b, t):
        # print("CUBINTER")
        # print(pos_a, pos_b)
        return tuple((self.inter(*args) for args in zip(pos_a, pos_b, repeat(t, 3))))

    @staticmethod
    def round_cube(pos):
        # x, y, z = pos
        rx, ry, rz = rpos = tuple(int(p) for p in pos)
        dx, dy, dz = (abs(p - rp) for p, rp in zip(pos, rpos))
        if dx > dy and dx > dz:
            rx = -ry - rz
        elif dy > dz:
            ry = -rx - rz
        else:
            rz = -rx - ry
        return int(rx), int(ry), int(rz)

    def get_line(self, source_cell, target_cell, length=None):
        # TODO правильно продлевать длину линий
        length = length or self.distance(source_cell, target_cell)
        result = []
        step = 1/length
        s_cube_pos = self.offsets_to_cube(source_cell.pos)
        t_cube_pos = self.offsets_to_cube(target_cell.pos)
        for i in range(length+1):
            cell = self[self.round_cube(self.cube_inter(s_cube_pos, t_cube_pos, step*i))]
            if cell is not None:
                result.append(cell)
            else:
                break
        return result

    def _get_generations(self, pos_or_cell, r):
        if not isinstance(pos_or_cell, Cell):
            cell = self[pos_or_cell]
        else:
            cell = pos_or_cell

        generations = [{cell}]
        for i in range(r):
            generations.append(
                reduce(lambda prev, x: prev | set(x.adjacent), generations[-1], set())
            )
        return generations

    def get_area(self, pos_or_cell, r):
        generations = self._get_generations(pos_or_cell, r)
        return reduce(lambda prev, x: prev | x, generations, set())

    def get_ring(self, pos_or_cell, r):
        generations = self._get_generations(pos_or_cell, r)
        return generations[-1] - (reduce(lambda prev, x: prev | x, generations[:-1:], set()))

    def __getitem__(self, item):
        if len(item) == 3:
            return self[self.cube_to_offsets(item)]
        else:
            q, r = item
            w, h = self.size
            # print(q, r)
            if q < w and r < h:
                return self._grid[q][r]
            else:
                return None

    def find_path(self, from_pos_or_cell, to_pos_or_cell):

        if isinstance(from_pos_or_cell, tuple):
            fcell = self[from_pos_or_cell]
        else:
            fcell = from_pos_or_cell

        if isinstance(to_pos_or_cell, tuple):
            tcell = self[to_pos_or_cell]
        else:
            tcell = to_pos_or_cell

        return self._find_path(fcell, tcell)

    def _find_path(self, fcell, tcell):
        paths = [[fcell]]
        already = set()
        while True:
            new_paths = []
            for path in paths:
                last_cell = path[-1]
                for cell in (cell for cell in last_cell.adjacent if cell not in already):
                    already.add(cell)
                    if cell is tcell:
                        return path + [cell]
                    else:
                        new_paths.append(path + [cell])
            if new_paths:
                paths = new_paths
            else:
                return []

    def __iter__(self):
        return iter(chain(*self._grid))

if __name__ == '__main__':
    grid = HexGrid((10, 10))
    print(grid.get_area((4, 4), 2))
