from .effect import (
    MetaEffect,
)
from ...replication_manager import MetaRegistry

TRIGGERS = MetaRegistry()['Trigger']
TriggerMeta = MetaRegistry().make_registered_metaclass('Trigger')


class Trigger(metaclass=TriggerMeta):

    name = ""
    events = {}

    def __init__(self, context=None):
        self.context = context

    def apply(self, event, target, context):
        effects = self.events.get(event, [])
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


def trigger_constructor(loader, node):
    t_s = loader.construct_mapping(node)
    name = t_s.pop("name")
    trigger = TRIGGERS[name](**t_s)
    return trigger


def new_trigger_constructor(loader, node):
    t_s = loader.construct_mapping(node)

    class NewTrigger(Trigger):
        name = t_s.pop("name")
        events = t_s

    return NewTrigger

TRIGGER_TAG = "!trigger"
NEW_TRIGGER_TAG = "!new_trigger"


# TRIGGERS = {}