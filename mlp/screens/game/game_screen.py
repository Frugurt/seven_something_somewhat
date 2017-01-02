from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import kivy.properties as prop


class GameScreen(Screen):

    app = prop.ObjectProperty()

    def __init__(self, app, game, network_manager, username="", **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.game = game
        self.username = username
        self.add_widget(self.game.make_widget(network_manager=network_manager))
