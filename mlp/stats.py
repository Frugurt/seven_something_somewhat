from collections import defaultdict
import traceback
from .resource import Resource
from .bind_widget import bind_widget
from .tools import dict_merge


PLANNING, ACTION = range(2)


# @bind_widget("Stats")
class Stats:

    hooks = ['load']

    def __init__(self, name, owner):#, is_presumed=False):
        self.state = PLANNING
        self.name = name
        self.owner = owner
        self.health = 100
        self.attack = 15
        self.initiative = 3
        self._action_points = Resource(3, 0, 3)
        self._move_points = Resource(3, 0, 3)
        self.unit_state = "sword"
        self.ammo = 3
        self.loaded = True
        self.parried = False
        self._triggers = defaultdict(dict)
        self.statuses = {}
        self.cell = None
        # self.presumed_stats = None if is_presumed else Stats(name, owner, True)
        # self.current_action_bar = CurrentActionBar(self.owner)

    @property
    def triggers(self):
        return self._triggers

    @triggers.setter
    def triggers(self, value):
        self._triggers = defaultdict(value)

    @property
    def action_points(self):
        return self._action_points.value

    @action_points.setter
    def action_points(self, v):
        self._action_points.value = v

    @property
    def move_points(self):
        return self._move_points.value

    @move_points.setter
    def move_points(self, v):
        self._move_points.value = v

    def take_damage(self, damage):
        self.health -= damage

    def load(self, struct):
        for key, value in struct.items():
            setattr(self, key, value)
        # print(self.statuses)

    def dump(self):
        struct = {
            "name": self.name,
            "health": self.health,
            "attack": self.attack,
            "action_points": self.action_points,
            "move_points": self.move_points,
            "initiative": self.initiative,
            "owner": self.owner,
            "unit_state": self.unit_state,
            "ammo": self.ammo,
            "loaded": self.loaded,
            "parried": self.parried,
            'cell': self.cell,
            'statuses': self.statuses.copy(),
            # "action": self.action.__class__.__name__ if self.action else ""
        }
        # if self.presumed_stats:
        #     struct.update({'presumed': self.presumed_stats.dump()})
        return struct


@bind_widget("Stats")
class MajorStats(Stats):

    def __init__(self, name, owner):
        super().__init__(name, owner)
        self.presumed = Stats(name, owner)

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