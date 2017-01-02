# -*- coding: utf-8 -*-
from kivy.lang import Builder
import kivy.uix.widget as widget
from kivy.uix import (
    relativelayout,
    # floatlayout,
    # layout,
    label,
)
from kivy.properties import (
    ListProperty,
    # ObjectProperty,
    NumericProperty,
    BooleanProperty,
)
from math import cos, sin, pi, sqrt


__author__ = 'ecialo'
H_COEF = sqrt(3)/2
SQ2 = sqrt(2)

Builder.load_file('./mlp/widgets/grid/rect_grid.kv')


class RectCellWidget(relativelayout.FloatLayout):

    mesh_vertices = ListProperty()
    circuit = ListProperty()
    # mesh_texture = ObjectProperty(None)
    hex_size = NumericProperty(40)
    is_selected = BooleanProperty(False)
    is_highlighted = BooleanProperty(False)

    def __init__(self, cell, **kwargs):
        # pos = self.grid_to_widget(kwargs['pos'])
        # texture = kwargs.pop('texture').texture
        # kwargs['pos'] = pos
        # print(kwargs)
        self.cell = cell
        super().__init__(
            size=(self.hex_size, self.hex_size),
            **kwargs
        )
        # self.register_event_type('on_get_cards')
        # self.center = self.pos
        # super().__init__(pos=pos, **kwargs)
        self.update_vertices()
        # self.mesh_texture = texture

    def on_take(self, obj):
        self.remove_widget(obj.make_widget())

    def on_place(self, obj):
        self.add_widget(obj.make_widget())

    def update_vertices(self):
        # print("update")
        vertices = []
        circuit = []
        step = 4
        istep = (pi * 2) / float(step)
        for i in range(step):
            x = cos(istep * i - pi/4) * self.hex_size + self.hex_size/2
            y = sin(istep * i - pi/4) * self.hex_size + self.hex_size/2
            vertices.extend([x, y, 0.5 + cos(istep * i)/2, 0.5 + sin(istep * i)/2])
            circuit.extend([x, y])
        self.mesh_vertices = vertices
        self.circuit = circuit + circuit[0:2]

    # def grid_to_widget(self, pos):
    #     size = self.hex_size
    #     col, row = pos
    #     x = size * 1.5 * col
    #     y = size * 1.5 * row
    #     return x, y

    def on_touch_down(self, touch):
        ret = False
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if self.collide_point(*touch.pos):
            self.parent.select_cell(self)
            # self.is_selected = not self.is_selected
            # for c in (c.make_widget() for c in self.cell.adjacent):
            #     c.is_selected = not c.is_selected
            #     print(c.cell.pos)
            ret = True
        touch.pop()
        return ret

    def collide_point(self, x, y):
        # print(self.pos, x, y)
        return sqrt(x*x + y*y) <= (self.hex_size/2)

    def to_local(self, x, y, relative=True):
        hhs = self.hex_size/2
        nx, ny = super().to_local(x, y, relative)
        return nx - hhs, ny - hhs


class RectGridWidget(widget.Widget):

    # cell_indices = list(range(4))
    cell_size = 40

    def __init__(self, grid, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        w, h = grid.size
        self._grid = [
            [None for _ in range(h)] for _ in range(w)]
        self.make_cells()

    def select_cell(self, cell):
        self.parent.cursor.select(cell)
        # print(cell.cell.pos)
        # try:
        #     self.selected_cell.is_selected = False
        # except AttributeError:
        #     pass
        # self.selected_cell = cell
        # cell.is_selected = True

    # def on_selected_cell(self, inst, cell):
    #     print(self.selected_cell, inst.selected_cell, cell)

    def make_cells(self):
        for cell in self.grid:
            pos = cell.pos
            terrain = cell.terrain
            x, y = pos
            w = cell.make_widget(pos=self.grid_to_window(pos))
            self._grid[x][y] = w
            self.add_widget(w)
            if terrain:
                t = terrain.make_widget(pos_hint={'center_x': 0.5, 'center_y': 0.5})
                w.add_widget(t)
                if cell.object:
                    o = cell.object.make_widget(pos_hint={'center_x': 0.5, 'center_y': 0.5})
                    w.add_widget(o)
                for _, content in enumerate(cell.additional_content):
                    c = content.make_widget(pos_hint={'center_x': 0.5, 'center_y': 0.5})
                    w.add_widget(c)
            w.add_widget(label.Label(text=str(pos), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

    def on_pos(self, inst, value):
        # print(self, new_pos, ololo)
        # super().on_pos(new_pos, ololo)
        for child in self.children:
            child.pos = self.grid_to_window(child.cell.pos)

    def grid_to_window(self, pos):
        sx, sy = self.pos
        size = self.cell_size
        col, row = pos
        x = size*1.5*col + sx
        y = size*1.5*row + sy
        # print(x, y)
        return x, y




        # self._grid = [
        #     [RectCellWidget(pos=(i, j), texture=hexgrid[i][j].texture, is_selected=hexgrid[i][j].is_selected) for j in range(h)] for i in range(w)]
        # for column in self._grid:
        #     for cell in column:
        #         self.add_widget(cell)


if __name__ == '__main__':
    from kivy.app import App
    from kivy.core.image import Image as CoreImage
    from kivy.uix.image import Image
    texture = CoreImage('/home/alessandro/PycharmProjects/mlp/grass.png')

    class CellMock(object):

        def __init__(self, i, j, texture_, is_selected=False):
            self.i = i
            self.j = j
            self.texture = texture_
            self.is_selected = is_selected

    h, w = 11, 11
    grid = [[CellMock(i, j, texture, i == 0 and j == 0) for j in range(h)] for i in range(w)]

    class TestApp(App):

        def build(self):
            wid = widget.Widget()
            grid_ = RectGridWidget(hexgrid=grid, pos=(0, 0))
            wid.add_widget(grid_)
            return wid

    TestApp().run()
