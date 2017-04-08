from .effect import (
    MetaEffect,
)
from ...replication_manager import MetaRegistry

TRIGGERS = MetaRegistry()['Trigger']
TriggerMeta = MetaRegistry().make_registered_metaclass('Trigger')


class Trigger(metaclass=TriggerMeta):

    name = ""
    events = []

    def __init__(self, context=None):
        self.context = context

    def apply(self, event, target, context):
        effects = getattr(self, event, [])
        # cell = target.stats.cell
        for effect in effects:
            if isinstance(effect, MetaEffect):
                effect.apply(target, self.context, effect_context=context)
            else:
                effect.apply(target.cell, self.context)

    def dump(self):
        return {
            'name': self.name,
            'context': self.context,
        }

    def __repr__(self):
        return "Trigger {}".format(self.name)


# TRIGGERS = {}