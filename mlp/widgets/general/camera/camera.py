from kivy.uix import (
    relativelayout,
    image,
    widget,
)
from kivy.properties import (
    # ObjectProperty,
    NumericProperty,
    ReferenceListProperty,
    BoundedNumericProperty
)
from kivy.lang import Builder
Builder.load_file('/home/alessandro/PycharmProjects/mlp/mlp/widgets/general/camera/camera.kv')


class Camera(relativelayout.RelativeLayout):
    # inner_pos = ObjectProperty((0, 0))
    inner_x = NumericProperty(0)
    inner_y = NumericProperty(0)
    normed_inner_x = BoundedNumericProperty(
        0.0, min=0.0, max=1.0,
        errorhandler=lambda x: min(1.0, max(0.0, x))
    )
    normed_inner_y = BoundedNumericProperty(
        0.0, min=0.0, max=1.0,
        errorhandler=lambda y: min(1.0, max(0.0, y))
    )
    zoom = NumericProperty(1.0)

    inner_pos = ReferenceListProperty(inner_x, inner_y)
    normed_inner_pos = ReferenceListProperty(normed_inner_x, normed_inner_y)

    def __init__(self, sub_widget, inner_pos=(0, 0), zoom=1.0, **kw):
        super().__init__(**kw)

        self.sub_widget = sub_widget
        # self.sub_size = sub_widget.size
        # print("Sub_Size", self.sub_size)

        self.inner_pos = inner_pos
        self.old_inner_pos = inner_pos
        self.min_zoom = max((c/e for c, e in zip(self.size, self.sub_size)))
        self.zoom = zoom

        self.bind(normed_inner_pos=self.pos_from_normed)
        # self.bind(inner_pos=self.normed_from_pos)
        self.bind(inner_pos=self.repos_subwidget)
        self.bind(zoom=self.rescale)

        # self.bind()

        self.add_widget(sub_widget)

    @property
    def sub_size(self):
        return self.sub_widget.size

    def pos_from_normed(self, _, normed_pos):
        print("Norm", normed_pos)
        sub_width, sub_height = self.sub_size
        x, y = (
            normed_pos[0]*(sub_width - self.width),
            normed_pos[1]*(sub_height - self.height)
        )
        print("SUB", self.sub_size)
        self.inner_pos = (x, y)
        # ox, oy = self.old_inner_pos
        # print("INNER POS")
        # print(x, ox, y, oy)
        # if abs(x - ox) + abs(y - oy) > 0.1:
        #     self.inner_pos = (x, y)

    def rescale(self, _, scale):
        if scale < self.min_zoom:
            self.zoom = self.min_zoom
        else:
            print("OLOLO")
            self.sub_widget.scale = scale
            self.pos_from_normed(None, self.normed_inner_pos)

    def normed_from_pos(self, pos):
        print("Hello")
        x, y = pos
        sw, sh = self.sub_size
        nx, ny = (
            x/(sw - self.width),
            y/(sh - self.height),
        )
        return nx, ny

    def repos_subwidget(self, _, pos):

        # print()
        # print(pos)
        # print(self.normed_inner_pos)
        # print(self.old_inner_pos)
        x, y = pos
        ox, oy = self.old_inner_pos
        sx, sy = self.sub_widget.pos
        self.sub_widget.pos = (
            sx - x + ox,
            sy - y + oy,
        )
        self.old_inner_pos = (x, y)

    # def scroll(self, dx, dy):
    #     ip = self.inner_pos
    #     self.inner_pos = (ip[0] + dx, ip[1] + dy)
    #     for child in self.children:
    #         child.x -= dx
    #         child.y -= dy
    #         print(child.pos)
    #     print(self.inner_pos)

    # def scale(self, ds):
    #     # print(ds)
    #     for child in self.children:
    #         # print(child.size)
    #         child.scale = ds


class FullImage(image.Image):
    scale = NumericProperty(1.0)
