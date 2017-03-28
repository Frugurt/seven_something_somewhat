class Trigger:

    name = ""
    events = []

    def __init__(self, source=None, **kwargs):
        self.source = source

    def apply(self, event, owner, target, *args, **kwargs):
        effects = getattr(self, event, [])
        # cell = target.stats.cell
        for effect in effects:
            effect.apply(target, self.source, *args, **kwargs)

    def dump(self):
        return {
            'name': self.name,
            'source': self.source,
        }

    def __repr__(self):
        return "Trigger {}".format(self.name)


TRIGGERS = {}