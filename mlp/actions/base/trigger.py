from .effect import (
    MetaEffect,
)
from ...replication_manager import MetaRegistry

TRIGGERS = MetaRegistry()['Trigger']
TriggerMeta = MetaRegistry().make_registered_metaclass('Trigger')


class Trigger(metaclass=TriggerMeta):

    name = ""
    events = []

    def __init__(self, source=None, **kwargs):
        self.source = source

    def apply(self, event, owner, target, *args, **kwargs):
        effects = getattr(self, event, [])
        # cell = target.stats.cell
        for effect in effects:
            if isinstance(effect, MetaEffect):
                effect.apply(target, self.source, *args, **kwargs)
            else:
                effect.apply(target.cell, self.source)

    def dump(self):
        return {
            'name': self.name,
            'source': self.source,
        }

    def __repr__(self):
        return "Trigger {}".format(self.name)


# TRIGGERS = {}