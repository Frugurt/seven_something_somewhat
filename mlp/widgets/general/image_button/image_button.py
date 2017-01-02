from kivy.app import App
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder

Builder.load_file('./mlp/widgets/general/image_button/image_button.kv')


class ImageButton(ButtonBehavior, Image):

    on_press_source = None
    on_release_source = None

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.source = self.on_release_source

    def on_press(self):
        self.source = self.on_press_source

    def on_release(self):
        self.source = self.on_release_source
