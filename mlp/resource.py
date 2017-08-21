from .bind_widget import bind_widget


class Resource:

    def dump(self):
        return self.value

    def load(self, v):
        self.value = v


@bind_widget("NumericResource")
class NumericResource(Resource):

    hooks = ['change']

    def __init__(self, name, initial, min_=0, max_=None):
        self.name = name
        self._current = initial
        self.min = min_
        self.max = max_ or initial

    @property
    def value(self):
        return self._current

    @value.setter
    def value(self, v):
        self._current = max(self.min, min(v, self.max))
        self.change()

    def change(self):
        pass

    # def dump(self):
    #     return self.value
    #
    # def load(self, v):
    #     self.value = v


class OptionResource(Resource):

    def __init__(self, inital, options):
        self._current = inital
        self.options = options

    @property
    def value(self):
        return self._current

    @value.setter
    def value(self, v):
        if v in self.options:
            self._current = v
        else:
            raise AttributeError()


class FlagResource(Resource):

    def __init__(self, initial):
        self._current = initial

    @property
    def value(self):
        return self._current

    @value.setter
    def value(self, v):
        if isinstance(v, bool):
            self._current = v
