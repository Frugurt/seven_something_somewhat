class Trigger:

    name = ""
    events = []

    def apply(self, event, target, *args, **kwargs):
        effects = getattr(self, event, [])
        cell = target.stats.cell
        for effect in effects:
            effect.apply(cell, *args, **kwargs)

TRIGGERS = {}