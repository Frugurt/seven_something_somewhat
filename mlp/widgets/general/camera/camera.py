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
Builder.load_file('./mlp/widgets/general/camera/camera.kv')


class Camera(relativelayout.RelativeLayout):

    def __init__(self, sub_widget, camera_pos=(0, 0), zoom=1.0, **kw):
        super().__init__(**kw)

        self.sub_widget = sub_widget

        self._camera_pos = (0, 0)
        self._normed_camera_pos = (0, 0)
        self._old_camera_pos = (0, 0)
        self._zoom = 0

        self.camera_pos = camera_pos
        self.zoom = zoom

        self.add_widget(sub_widget)

    @property
    def camera_pos(self):
        return self.camera_pos

    @camera_pos.setter
    def camera_pos(self, value):
        self._camera_pos = value
        self._normed_camera_pos = self.normed_from_pos(value)
        self.repos_subwidget(value)

    @property
    def camera_x(self):
        return self._camera_pos[0]

    @camera_x.setter
    def camera_x(self, value):
        self.camera_pos = (value, self._camera_pos[1])

    @property
    def camera_y(self):
        return self._camera_pos[1]

    @camera_y.setter
    def camera_y(self, value):
        self.camera_pos = (self._camera_pos[0], value)

    @property
    def normed_camera_pos(self):
        return self._normed_camera_pos

    @normed_camera_pos.setter
    def normed_camera_pos(self, value):
        self._normed_camera_pos = value
        self._camera_pos = self.pos_from_normed(value)
        self.repos_subwidget(self._camera_pos)

    @property
    def normed_camera_x(self):
        return self._normed_camera_pos[0]

    @normed_camera_x.setter
    def normed_camera_x(self, value):
        self.camera_pos = (value, self._normed_camera_pos[1])

    @property
    def normed_camera_y(self):
        return self._normed_camera_pos[1]

    @normed_camera_y.setter
    def normed_camera_y(self, value):
        self.camera_pos = (self._normed_camera_pos[0], value)

    @property
    def sub_size(self):
        return self.sub_widget.size

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        self.rescale(value)

    def pos_from_normed(self, normed_pos):
        sub_width, sub_height = self.sub_size
        x, y = (
            normed_pos[0]*(sub_width - self.width),
            normed_pos[1]*(sub_height - self.height)
        )
        return x, y

    def rescale(self, scale):
        self.sub_widget.scale = scale
        self.normed_camera_pos = self.normed_camera_pos

    def normed_from_pos(self, pos):
        # print("Hello")
        x, y = pos
        sw, sh = self.sub_size
        nx, ny = (
            x/(sw - self.width),
            y/(sh - self.height),
        )
        return nx, ny

    def repos_subwidget(self, pos):
        x, y = pos
        ox, oy = self._old_camera_pos
        sx, sy = self.sub_widget.pos
        self.sub_widget.pos = (
            sx - x + ox,
            sy - y + oy,
        )
        self._old_camera_pos = (x, y)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrollup':
                self.zoom -= 0.05
            else:
                self.zoom += 0.05
            return False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        x, y = self._camera_pos
        self.camera_pos = (x - touch.dx, y - touch.dy)
        return False

    # def on_touch_up(self, touch):
    #     pass


class FullImage(image.Image):
    scale = NumericProperty(1.0)
