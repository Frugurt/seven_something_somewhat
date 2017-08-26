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


class NumericResource(Resource):
    value = NumericProperty()
    max_value = NumericProperty()
    name = StringProperty()

    # def __init__(self, name, value, max_value=None, **kwargs):
    def __init__(self, resource, **kwargs):
        super().__init__(**kwargs)
        self.resource = resource
        self.name = resource.name_
        self.value = resource.value
        self.max_value = resource.max


class StringResource(Resource):

    value = StringProperty()
    name = StringProperty()

    def __init__(self, resource, **kwargs):
        super().__init__(**kwargs)
        self.resource = resource
        self.name = resource.name_
        self.value = resource.value


class BooleanResource(Resource):
    value = BooleanProperty()
    name = StringProperty()

    def __init__(self, resource, **kwargs):
        super().__init__(**kwargs)
        self.resource = resource
        self.name = resource.name_
        self.value = resource.value


