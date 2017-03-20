from kivy.uix.image import Image


class Unit(Image):

    def __init__(self, unit, **kwargs):
        super().__init__(**kwargs)
        self.unit = unit

    def on_select(self, game_widget):
        print(self.unit.action_bar)
        game_widget.stats = self.unit._stats.make_widget(pos_hint={'x': 0.0, 'y': 0.5})
        game_widget.add_widget(game_widget.stats)
        if game_widget.parent.username == self.unit.stats.owner or game_widget.parent.username == 'overlord':
            game_widget.action_bar = self.unit.action_bar.make_widget(
                pos_hint={'x': 0.0, 'bottom': 0.0},
            )
            game_widget.current_action_bar = self.unit.current_action_bar.make_widget(
                pos_hint={'x': 0.0, 'y': 0.1}
            )
            game_widget.add_widget(game_widget.action_bar)
            game_widget.add_widget(game_widget.current_action_bar)
            # self.center = self.pos

    # def on_place_in_cell(self, cell):
    #     if self.parent:
    #         pass