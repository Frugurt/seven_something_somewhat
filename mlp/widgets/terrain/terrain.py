from math import cos, sin, pi, sqrt
import numpy as np
from kivy.uix import (
    widget
)
from kivy.lang import Builder
from kivy.properties import (
    ListProperty,
    ObjectProperty,
    NumericProperty,
    BooleanProperty,
)

Builder.load_file('./mlp/widgets/terrain/terrain.kv')


class Terrain(widget.Widget):

    mesh_vertices = ListProperty([])
    mesh_texture = ObjectProperty(None)
    hex_size = NumericProperty(40)
    is_selected = BooleanProperty(False)
    texture = None

    def __init__(self, terrain, **kwargs):
        super().__init__(**kwargs)
        self.terrain = terrain
        self.mesh_texture = self.texture.texture
        # self.update_vertices()

    @property
    def rotator(self):
        return self.parent.rotator

    def on_pos(self, _, __):
        self.mesh_vertices = self.parent.mesh_vertices
        # self.update_vertices()

    # def update_vertices(self):
    #     vertices = []
    #     step = 4
    #     istep = (pi * 2) / float(step)
    #     for i in range(step):
    #         x = cos(istep * i - pi/4) * self.hex_size + self.hex_size/2
    #         y = sin(istep * i - pi/4) * self.hex_size + self.hex_size/2
    #         vertices.extend([x, y, 0.5 + cos(istep * i)/2, 0.5 + sin(istep * i)/2])
    #     self.mesh_vertices = vertices

    # def update_vertices(self):
        # vertices = []
        # points = []
        # indices = []
        # step = 6
        # istep = (pi * 2) / float(step)
        # # xx, yy = self.pos
        # for i in range(step):
        #     x = cos(istep * i) * self.hex_size
        #     y = sin(istep * i) * self.hex_size
        #
        #     c = np.matrix([[x], [y], [0]])
        #     m = (self.rotator @ c)
        #     nx, ny = m[0, 0], m[1, 0]
        #     x, y = nx, ny
        #     # print(m.shape)
        #
        #     vertices.extend([x, y, 0.5 + cos(istep * i)/2, 0.5 + sin(istep * i)/2])
        #     # points.extend([x, y])
        #     # indices.append(i)
        # # print id(self.mesh_vertices)
        # # self.circuit = points + points[0:2]
        # self.mesh_vertices = vertices

    # def on_pos(self, _, __):
        # self.update_vertices()