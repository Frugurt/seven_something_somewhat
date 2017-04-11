import kivy.properties as prop
import kivy.uix.widget as widget
import kivy.uix.gridlayout as grl
from kivy.lang import Builder
from .resource import (
    NumericResource,
    StringResource,
    BooleanResource,
)
from kivy.uix.label import Label
Builder.load_file('./mlp/widgets/stats/stats.kv')


# class Stats(grl.GridLayout):
#
#     health = prop.NumericProperty()
#     attack = prop.NumericProperty()
#     name = prop.StringProperty()
#     # action = prop.ObjectProperty()
#     owner = prop.StringProperty()
#     action_points = prop.NumericProperty()
#     move_points = prop.NumericProperty()
#     initiative = prop.NumericProperty()
#     unit_state = prop.StringProperty()
#     ammo = prop.NumericProperty()
#     loaded = prop.BooleanProperty()
#
#     def __init__(self, stats, *args, **kwargs):
#         super().__init__(**kwargs)
#         self.stats = stats
#         self.health = stats.health
#         self.name = stats.name
#         # self.action = stats.action
#         self.owner = stats.owner
#         self.action_points = stats.action_points
#         # self.move_points = stats.move_points
#         self.initiative = stats.initiative
#         self.unit_state = stats.unit_state
#         self.ammo = stats.ammo
#         self.loaded = stats.loaded
#
#     # def on_take_damage(self, _):
#     #     self.health = self.stats.health
#
#     def on_load(self, struct):
#         print(struct)
#         for key in struct['resources']:
#             setattr(self, key, getattr(self.stats, key))
#

class Stats(grl.GridLayout):

    def __init__(self, stats, *args, **kwargs):
        super().__init__(**kwargs)
        self.stats = stats
        self.resources = {}
        self.add_widget(Label(text="Name: {}".format(stats.name)))
        self.add_widget(Label(text="Owner: {}".format(stats.owner)))
        for res_name, value in stats.resources.items():
            if isinstance(value, bool):
                resource = BooleanResource(res_name, value)
            elif isinstance(value, str):
                resource = StringResource(res_name, value)
            else:
                resource = NumericResource(res_name, value)
            self.resources[res_name] = resource
            self.add_widget(resource)

    def on_load(self, struct):
        for key in struct['resources']:
            self.resources[key].value = self.stats.resources[key]