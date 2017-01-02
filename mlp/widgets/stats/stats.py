import kivy.properties as prop
import kivy.uix.widget as widget
import kivy.uix.gridlayout as grl
from kivy.lang import Builder
Builder.load_file('./mlp/widgets/stats/stats.kv')


class Stats(grl.GridLayout):

    health = prop.NumericProperty()
    attack = prop.NumericProperty()
    name = prop.StringProperty()
    # action = prop.ObjectProperty()
    owner = prop.StringProperty()
    action_points = prop.NumericProperty()
    move_points = prop.NumericProperty()
    initiative = prop.NumericProperty()
    unit_state = prop.StringProperty()
    ammo = prop.NumericProperty()
    loaded = prop.BooleanProperty()

    def __init__(self, stats, *args, **kwargs):
        super().__init__(**kwargs)
        self.stats = stats
        self.health = stats.health
        self.name = stats.name
        # self.action = stats.action
        self.owner = stats.owner
        self.action_points = stats.action_points
        self.move_points = stats.move_points
        self.initiative = stats.initiative
        self.unit_state = stats.unit_state
        self.ammo = stats.ammo
        self.loaded = stats.loaded

    # def on_take_damage(self, _):
    #     self.health = self.stats.health

    def on_load(self, struct):
        print(struct)
        for key in struct:
            setattr(self, key, getattr(self.stats, key))
