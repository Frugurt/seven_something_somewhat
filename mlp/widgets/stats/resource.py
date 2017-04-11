from kivy.uix.label import Label
from kivy.properties import (
    NumericProperty,
    StringProperty,
    BooleanProperty,
)
from kivy.lang import Builder
Builder.load_file('./mlp/widgets/stats/resource.kv')


class NumericResource(Label):

    value = NumericProperty()
    max_value = NumericProperty()
    name = StringProperty()

    def __init__(self, name, value, max_value=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.value = value
        self.max_value = max_value or value


class StringResource(Label):

    value = StringProperty()
    name = StringProperty()

    def __init__(self, name, value, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.value = value


class BooleanResource(Label):
    value = BooleanProperty()
    name = StringProperty()

    def __init__(self, name, value, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.value = value


