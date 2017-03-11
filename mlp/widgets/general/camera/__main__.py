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

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode, text, modifiers)
        dx, dy = 0, 0
        ds = 0.0
        if keycode[1] == 'w':
            dy += 10
        elif keycode[1] == 's':
            dy -= 10
        elif keycode[1] == 'a':
            dx -= 10
        elif keycode[1] == 'd':
            dx += 10
        elif keycode[1] == 'numpadadd':
            ds += 0.1
        elif keycode[1] == 'numpadsubstract':
            ds -= 0.1
        # print(self.zoom)
        self.zoom += ds
        self.camera.scroll(dx, dy)
        self.camera.scale(self.zoom)
        return False

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def build(self):
        wid = Camera()
        self.camera = wid
        wid.add_widget(FullImage(source="./data/fonchik_pustynka1.png"))
        return wid


TestApp().run()
