from .bind_widget import bind_widget
from .replication_manager import MetaRegistry

RESOURCES = MetaRegistry()['Resource']
ResourceMeta = MetaRegistry().make_registered_metaclass("Resource")


class Resource(metaclass=ResourceMeta):

    hooks = ['change']

    def dump(self):
        return self.value

    def load(self, v):
        self.value = v

    def change(self):
        """
        Используется для передачи сигнала об обновлении виджетов
        """
        pass


@bind_widget("NumericResource")
class NumericResource(Resource):

    name = "numeric"

    def __init__(self, name, initial, min=0, max=None):
        self.name = name
        self._current = initial
        self.min = min
        self.max = max or initial

    @property
    def value(self):
        return self._current

    @value.setter
    def value(self, v):
        self._current = max(self.min, min(v, self.max))
        self.change()

    # def dump(self):
    #     return self.value
    #
    # def load(self, v):
    #     self.value = v


@bind_widget("StringResource")
class OptionResource(Resource):

    name = "option"

    def __init__(self, name, initial, options):
        self.name = name
        self._current = initial
        self.options = options

    @property
    def value(self):
        return self._current

    @value.setter
    def value(self, v):
        if v in self.options:
            self._current = v
            self.change()
        else:
            raise AttributeError("value not in {}".format(self.options))


@bind_widget("BooleanResource")
class FlagResource(Resource):

    name = "flag"

    def __init__(self, name, initial):
        self.name = name
        self._current = initial

    @property
    def value(self):
        return self._current

    @value.setter
    def value(self, v):
        if isinstance(v, bool):
            self._current = v
            self.change()

RESOURCE_TABLE = {
    int: NumericResource,
    bool: FlagResource,
}


def resource_constructor(loader, node):
    r_s = loader.construct_mapping(node)
    name = r_s.pop("type")
    resource = RESOURCES[name](name, **r_s)
    return resource

RESOURCE_TAG = "!res"
