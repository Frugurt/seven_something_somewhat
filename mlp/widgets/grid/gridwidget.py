# -*- coding: utf-8 -*-
import kivy
from kivy.uix import (
    layout
)
import kivy.uix.boxlayout as blayout
import numpy as np
from numpy import matlib as mtl
from kivy.lang import Builder
import kivy.uix.widget as widget
from kivy.uix import (
    relativelayout,
    floatlayout,
    label,
)
from kivy.properties import (
    ListProperty,
    ObjectProperty,
    NumericProperty,
    BooleanProperty,
)
import os
from kivy.factory import Factory
from kivy.uix.slider import Slider
from kivy.graphics import Mesh, Color, Translate
from math import cos, sin, pi, sqrt, degrees, radians
from kivy.uix.image import Image
# from ..general.camera.camera import FullImage
from ..unit.unit import Unit
import random as rnd
from kivy.uix.filechooser import *
from kivy.uix.popup import Popup
__author__ = 'ecialo'
H_COEF = sqrt(3)/2
R2 = radians(60)

# Factory.register('LoadDialog', cls=LoadDialog)

Builder.load_file('./mlp/widgets/grid/gridwidget.kv')


# class LoadDialog(floatlayout.FloatLayout):
#     load = ObjectProperty(None)
#     cancel = ObjectProperty(None)


def in_polygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y < yp[i-1]) or (yp[i-1] <= y < yp[i])) and
           (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])):
                c = 1 - c
    return bool(c)


class HexCellWidget(relativelayout.FloatLayout):

    mesh_vertices = ListProperty([])
    circuit = ListProperty([])
    # mesh_texture = ObjectProperty(None)
    # hex_size = NumericProperty()
    is_selected = BooleanProperty(False)
    is_highlighted = BooleanProperty(False)
    rotator = mtl.eye(3)

    def __init__(self, cell, **kwargs):
        self.cell = cell
        hex_size = kwargs.pop('hex_size')
        # self.cell_pos = kwargs.pop('cell_pos')
        super(HexCellWidget, self).__init__(
            size=(hex_size*2, hex_size*2),
            **kwargs
        )
        # self.hex_size = hex_size
        # self.update_vertices()
        # self.bind(rotator=self.update_vertices)

    def on_take(self, obj):
        self.remove_widget(obj.make_widget())

    def on_place(self, obj):
        self.add_widget(obj.make_widget())

    # def on_pos(self, _, __):
    #     if self.parent:
    #         self.update_vertices()

    @property
    def hex_size(self):
        return self.parent.cell_size

    def update_vertices(self):
        # print("UPDATE")
        vertices = []
        points = []
        # indices = []
        step = 6
        istep = (pi * 2) / float(step)
        xs = []
        ys = []
        for i in range(step):
            x = cos(istep * i) * self.hex_size + self.hex_size
            y = sin(istep * i) * self.hex_size + self.hex_size*H_COEF

            c = np.matrix([[x], [y], [0]])
            m = (self.rotator * c)
            nx, ny = m[0, 0], m[1, 0]
            x, y = nx, ny
            # print(m.shape)

            vertices.extend([x, y, 0.5 + cos(istep * i)/2, 0.5 + sin(istep * i)/2])
            points.extend([x, y])
            xs.append(x)
            ys.append(y)
            # indices.append(i)
        # print id(self.mesh_vertices)
        self.circuit = points + points[0:2]
        self.mesh_vertices = vertices
        self.size = (int(max(xs) - min(xs)), int(max(ys) - min(ys)))
        for child in self.children:
            if isinstance(child, Unit):
                # print("\n\nSCALE", 123)
                child.scale = self.parent.scale * child.default_scale

    # def on_pos(self, _, __):
    #     for child in self.children:
    #         try:
    #             child.update_verticies()
    #         except AttributeError:
    #             pass

    @property
    def cell_pos(self):
        return self.cell.pos

    def on_touch_down(self, touch):
        ret = False
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if self.collide_point(*touch.pos):
            self.parent.select_cell(self)
            ret = True
        touch.pop()
        return ret

    def collide_point(self, x, y):
        xs = self.mesh_vertices[::4]
        ys = self.mesh_vertices[1::4]
        # print(x, y)
        # print(xs[0], ys[0])
        return in_polygon(x, y, xs, ys)

    def to_local(self, x, y, relative=True):
        return super().to_local(x, y, relative)


class Hexgrid(widget.Widget):

    cell_indices = range(6)
    cell_size = NumericProperty(110)
    base_cell_size = 110
    rotation = NumericProperty(0)
    rotator = mtl.eye(3)
    scale = NumericProperty(1.0)

    def __init__(self, grid, **kwargs):
        # hexgrid = kwargs.pop('hexgrid')
        hexgrid = grid
        self.grid = grid
        self.hexgrid = hexgrid
        w, h = len(hexgrid._grid), len(hexgrid._grid[0])
        self._grid = [
            [None for _ in range(h)] for _ in range(w)]
        super(Hexgrid, self).__init__(
            # size=(),
            **kwargs
        )
        self.make_cells()
        # self.size = self.ids.background.size
        # for column in self._grid:
        #     for cell in column:
        #         self.add_widget(cell)
        # self.update_children()
        self.bind(rotation=self.change_rotator)
        self.bind(cell_size=self.update_children)
        self.bind(scale=self.rescale)
        # child_size = (0, 0)
        self.update_size()

    def make_cells(self):
        for cell in reversed(list(self.grid)):
            pos = cell.pos
            terrain = cell.terrain
            x, y = pos
            w = cell.make_widget(
                hex_size=self.cell_size,
                pos=self.grid_to_window(pos)
            )
            self._grid[x][y] = w
            self.add_widget(w)
            if terrain:
                # t = terrain.make_widget(pos_hint={'center_x': 0.5, 'center_y': 0.5})
                # w.add_widget(t)
                # t.update_vertices()
                if cell.object:
                    o = cell.object.make_widget(pos_hint={'center_x': 0.5, 'y': 0.3})
                    w.add_widget(o)
                # for _, content in enumerate(cell.additional_content):
                #     c = content.make_widget(pos_hint={'center_x': 0.5, 'center_y': 0.5})
                #     w.add_widget(c)
            w.add_widget(label.Label(text=str(pos), pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.update_children()

    def change_rotator(self, _, value):
        rad = radians(value)
        self.rotator = np.matrix([
            [1.0, 0.0, 0.0],
            [0.0, cos(rad), sin(rad)],
            [0.0, -sin(rad), cos(rad)]
        ])
        for child in self.children:
            if isinstance(child, HexCellWidget):
                child.rotator = self.rotator
        self.update_children()
        # self.slider = Slider(pos=(100, 100), )

    def update_size(self):
        xs = []
        ys = []
        self.rotation = 56
        for child in self.children:
            xs.append(child.x)
            ys.append(child.y)
        width, height = self._grid[0][0].size
        self.size = (int(max(xs) - min(xs)) + width, int(max(ys) - min(ys)) + height)

    def on_pos(self, inst, value):
        self.update_children()

    def rescale(self, _, scale):
        # print(self.scale)
        self.cell_size = self.base_cell_size*scale
        self.update_size()
        # self.center_x = self.parent.width/2
        # self.center_y = self.parent.height/2

    def update_children(self, _=None, __=None):
        for child in self.children:
            if isinstance(child, HexCellWidget):
                child.pos = self.grid_to_window(child.cell_pos)
                child.update_vertices()

    def grid_to_window(self, pos):
        sx, sy = self.pos
        size = self.cell_size
        col, row = pos
        # print(col, row, type(col), type(row))
        x = size * 3 / 2 * col
        y = size * sqrt(3) * (row - 0.5 * (col & 1))

        # print(x, y)
        x, y = sx+x, sy+y
        # print(x, y)
        c = np.matrix([[x], [y], [0]])
        # R2 = radians(45)
        m = (self.rotator * c)
        # print(m)
        nx, ny = m[0, 0], m[1, 0]
        x, y = float(nx), float(ny)
        return x, y

    def select_cell(self, cell):
        self.parent.cursor.select(cell)


class FullImage(Image):
    pass


class CompositeArena(relativelayout.RelativeLayout):

    def __init__(self, gridwidget, **kwargs):
        super().__init__(**kwargs)
        self.gridwidget = gridwidget
        self.add_widget(gridwidget)
        self.bind(scale=self.rescale)

    def rescale(self, _, scale):
        self.gridwidget.scale = scale

    @property
    def cursor(self):
        return self.parent.parent.cursor

# class RotateGridWidget(widget.Widget):
#
#     def show_load_background(self):
#         content = LoadDialog(load=self.load_background, cancel=self.dismiss_popup)
#         self._popup = Popup(title="Load background", content=content,
#                             size_hint=(0.9, 0.9))
#         self._popup.open()
#
#     def show_load_model(self):
#         content = LoadDialog(load=self.load_model, cancel=self.dismiss_popup)
#         self._popup = Popup(title="Load model", content=content,
#                             size_hint=(0.9, 0.9))
#         self._popup.open()
#
#     def load_background(self, path, filename):
#         back_texture = os.path.join(path, filename[0])
#         try:
#             texture = CoreImage(back_texture).texture
#             self.ids.background.texture = texture
#         except:
#             pass
#         self._popup.dismiss()
#
#     def load_model(self, path, filename):
#         back_texture = os.path.join(path, filename[0])
#         try:
#             texture = CoreImage(back_texture).texture
#             self.ids.model.texture = texture
#         except:
#             pass
#         self._popup.dismiss()
#
#     def dismiss_popup(self):
#         self._popup.dismiss()

