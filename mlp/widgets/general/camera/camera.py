from kivy.uix import (
    relativelayout,
    image,
    widget,
)
from kivy.properties import (
    # ObjectProperty,
    NumericProperty,
    ReferenceListProperty,
)
from kivy.lang import Builder
Builder.load_file('/home/alessandro/PycharmProjects/mlp/mlp/widgets/general/camera/camera.kv')


class Camera(relativelayout.RelativeLayout):
    # inner_pos = ObjectProperty((0, 0))
    inner_x = NumericProperty(0)
    inner_y = NumericProperty(0)
    zoom = NumericProperty(1.0)

    inner_pos = ReferenceListProperty(inner_x, inner_y)

    def __init__(self, inner_pos=(0, 0), zoom=1.0, **kw):
        super().__init__(**kw)
        self.inner_pos = inner_pos
        self.zoom = zoom

    def scroll(self, dx, dy):
        ip = self.inner_pos
        self.inner_pos = (ip[0] + dx, ip[1] + dy)
        for child in self.children:
            child.x -= dx
            child.y -= dy

    def scale(self, ds):
        print(ds)
        for child in self.children:
            print(child.size)
            child.scale = ds


class FullImage(image.Image):
    scale = NumericProperty(1.0)
