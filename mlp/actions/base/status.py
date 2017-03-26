class Status:

    name = None

    def __init__(self, **kwargs):
        pass
        # self.source = source

    def on_add(self, target):
        pass

    def on_remove(self, target):
        pass

    def dump(self):
        return {
            "name": self.name,
            # "source": self.source,
        }

STATUSES = {}
