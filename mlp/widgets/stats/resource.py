from kivy.uix.label import Label
from kivy.properties import (
    NumericProperty,
    StringProperty,
    BooleanProperty,
    Property,
)
from kivy.lang import Builder
Builder.load_file('./mlp/widgets/stats/resource.kv')


class Resource(Label):
    value = None

    def on_change(self, _):
        self.value = self.resource.value


class NumericResource(Label):
    value = NumericProperty()
    max_value = NumericProperty()
    name = StringProperty()

    # def __init__(self, name, value, max_value=None, **kwargs):
    def __init__(self, resource, **kwargs):
        super().__init__(**kwargs)
        self.resource = resource
        self.name = resource.name
        self.value = resource.value
        self.max_value = resource.max


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


