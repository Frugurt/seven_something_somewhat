class Resource:

    def dump(self):
        return self.value

    def load(self, v):
        self.value = v


class NumericResource(Resource):

    def __init__(self, inital, min_=0, max_=None):
        self._current = inital
        self.min = min_
        self.max = max_ or inital
        self.base = inital      # для работы с модификаторами, которых сейчас нет

    @property
    def value(self):
        return self._current

    @value.setter
    def value(self, v):
        self._current = max(self.min, min(v, self.max))

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