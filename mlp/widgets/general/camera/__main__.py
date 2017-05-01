from kivy.app import App
from .camera import (
    Camera,
    FullImage,
)
from kivy.core.window import Window


class TestApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.zoom = 1.0
        self.nx = 0.0
        self.ny = 0.0

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode, text, modifiers)
        dx, dy = 0, 0
        ds = 0.0
        if keycode[1] == 'w':
            # self.ny += 0.01
            dy += 0.01
            # dy += 10
        elif keycode[1] == 's':
            # self.ny -= 0.01
            dy -= 0.01
            # dy -= 10
        elif keycode[1] == 'a':
            # self.nx -= 0.01
            dx -= 0.01
            # dx -= 10
        elif keycode[1] == 'd':
            # self.nx += 0.01
            dx += 0.01
            # dx += 10
        elif keycode[1] == 'numpadadd':
            ds += 0.01
        elif keycode[1] == 'numpadsubstract':
            ds -= 0.01
        # print(self.zoom)
        self.camera.zoom += ds
        # self.camera.normed_inner_x = self.nx
        # self.camera.normed_inner_y = self.ny
        ix, iy = self.camera.normed_camera_pos
        # print("get", (ix, iy))
        self.camera.normed_camera_pos = (ix + dx, iy + dy)
        # self.camera.inner_pos = (ix + dx, iy + dy)
        return False

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def build(self):
        wid = FullImage(source="./data/fonchik_pustynka1.png")
        self.camera = Camera(wid, pos=(100, 100))#, size_hint=(None, None), size=(1024, 768))
        return self.camera


TestApp().run()
