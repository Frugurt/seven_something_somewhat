class Resource:

    def __init__(self, inital, min_, max_):
        self._current = inital
        self.min = min_
        self.max = max_

    @property
    def value(self):
        return self._current

    @value.setter
    def value(self, v):
        self._current = max(self.min, min(v, self.max))

    def dump(self):
        return self.value

    def load(self, v):
        self.value = v
