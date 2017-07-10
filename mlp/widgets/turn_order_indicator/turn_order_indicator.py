import kivy.properties as prop
import kivy.uix.widget as widget
import kivy.uix.gridlayout as grl
import  kivy.uix.stacklayout as stl
import kivy.uix.label as label
import kivy.uix.widget
from kivy.lang import Builder

Builder.load_file('./mlp/widgets/turn_order_indicator/turn_order_indicator.kv')


class TurnOrderRecord(widget.Widget):

    text = prop.StringProperty()

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text


class TurnOrderIndicator(stl.StackLayout):

    def __init__(self, turn_order_manager, **kwargs):
        self.turn_order_manager = turn_order_manager
        super().__init__(**kwargs)
        for u in self.turn_order_manager:
            self.add_widget(TurnOrderRecord(text="{} {}".format(u.stats.owner, u.name)))

    def on_load(self, _):
        self.clear_widgets()
        for u in self.turn_order_manager:
            self.add_widget(TurnOrderRecord(text="{} {}".format(u.stats.owner, u.name)))
