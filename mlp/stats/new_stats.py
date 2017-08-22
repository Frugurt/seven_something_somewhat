from collections import defaultdict
from .stats import (
    PLANNING
)
from ..actions.action import ActionBar
from ..tools import dict_merge
from ..bind_widget import bind_widget
from ..resource import (
    Resource,
    RESOURCE_TABLE,
)


class Stats:

    hooks = ['load']

    def __init__(self, owner, owner_name, resources):#, is_presumed=False):
        self.resources = resources.copy()
        self.state = PLANNING
        self.name = owner.__class__.__name__
        self.owner = owner_name
        self._triggers = defaultdict(dict)
        self.statuses = {}
        self.cell = None
        self.action_bar = ActionBar(owner)
        for key, value in self.resources.items():
            setattr(self, key, value)

    @property
    def triggers(self):
        return self._triggers

    @triggers.setter
    def triggers(self, value):
        self._triggers = defaultdict(value)

    def load(self, struct):
        action_bar = struct.pop("action_bar")
        self.action_bar.load(action_bar)
        for key, value in struct.items():
            setattr(self, key, value)
        for key, value in self.resources.items():
            setattr(self, key, value)
        struct["action_bar"] = action_bar
        # print(self.statuses)

    def dump(self):
        # status = self.statuses.copy()
        struct = {
            "name": self.name,
            "owner": self.owner,
            'cell': self.cell,
            'statuses': self.statuses.copy(),
            'resources': self.resources.copy(),
            'action_bar': self.action_bar.dump(),
        }
        return struct

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self.resources:
            self.resources[key] = value

    def __repr__(self):
        return "Stats with resources {}".format(self.resources)


@bind_widget("Stats")
class MajorStats(Stats):

    def __init__(self, name, owner, resources):
        super().__init__(name, owner, resources)
        self.presumed = Stats(name, owner, resources)

    def load(self, struct):
        presumed = struct.pop('presumed')
        self.presumed.load(presumed)
        super().load(struct)

    def dump(self):
        return dict_merge(
            super().dump(),
            {'presumed': self.presumed.dump()}
        )

    def update_presumed(self):
        struct = self.dump()
        struct.pop('presumed')
        self.presumed.load(struct)

    def __repr__(self):
        return "Major stats with resources {}".format(self.resources)
