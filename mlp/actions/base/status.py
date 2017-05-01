from ...replication_manager import MetaRegistry
from ...tools import (
    convert,
    dotdict,
)
from contextlib import contextmanager
from ..property.property import (
    Property,
    # Const,
)
from .effect import MetaEffect

STATUSES = MetaRegistry()["Status"]
StatusMeta = MetaRegistry().make_registered_metaclass("Status")


class Status(metaclass=StatusMeta):

    name = None
    events = {}
    on_add_effects = []
    on_remove_effects = []
    params = []

    def __init__(self, context=None, duration=-1, **kwargs):
        self.context = context
        self.duration = duration
        for k, v in kwargs.items():
            setattr(self, k, v)

    def configure(self, context):
        # context = context.copy()
        # context['status'] = self
        context_values = {}
        for k, v in vars(self).items():
            if isinstance(v, Property):
                context_values[k] = v.get(context)
            else:
                context_values[k] = v
        new_status = self.__class__(**context_values)
        context = context.copy()
        context['status'] = new_status
        new_status.context = context
        return new_status

    def on_add(self, target):
        for effect in self.on_add_effects:
            effect.apply(target.cell, self.context)

    def on_remove(self, target):
        for effect in self.on_remove_effects:
            effect.apply(target.cell, self.context)

    def tick(self):
        self.duration -= 1
        if self.duration == -1:
            self.context['target'].remove_status(self)

    def dump(self):
        return {
            "name": self.name,
            "params": vars(self),
        }

    def apply(self, event, target, context):
        effects = self.events.get(event, [])
        for effect in effects:
            if isinstance(effect, MetaEffect):
                effect.apply(target, self.context, effect_context=context)
            else:
                effect.apply(target.cell, self.context)

    def __repr__(self):
        return "Status {}".format(self.name)

    def copy(self):
        return self.__class__(**vars(self))


# class CustomStatus(Status):
#
#     on_add_effects = []
#     on_remove_effects = []
#
#     def __init__(self, context=None, duration=-1, **kwargs):
#         super().__init__(context, duration)
#         for k, v in kwargs.items():
#             setattr(self, k, v)
#
#     def on_add(self, target):
#         with self.configure(self.context) as c:
        # for effect in self.on_add_effects:
        #     effect.apply(target.stats.cell, self.context)
        #     TODO переписать эффекты, чтобы можно было просто передать цель
    #
    # def on_remove(self, target):
    #     for effect in self.on_remove_effects:
    #         effect.apply(target.stats.cell, self.context)


def status_constructor(loader, node):
    s_s = loader.construct_mapping(node)
    name = s_s.pop("name")
    status = STATUSES[name](**s_s)
    return status

STATUS_TAG = "!status"


def new_status_constructor(loader, node):
    s_s = loader.construct_mapping(node)

    class NewStatus(Status):

        name = s_s.pop("name")
        on_add_effects = s_s.pop("on_add", [])
        on_remove_effects = s_s.pop("on_remove", [])
        params = s_s.pop("params", [])
        events = {frozenset(k.split("_")[1::]): v for k, v in s_s.items()}

    return NewStatus

NEW_STATUS_TAG = "!new_status"
