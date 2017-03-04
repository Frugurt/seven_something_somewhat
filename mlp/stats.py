from collections import defaultdict
from .resource import Resource
from .bind_widget import bind_widget


@bind_widget("Stats")
class Stats:

    hooks = ['load']

    def __init__(self, name, owner):
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
        self.triggers = defaultdict(list)
        self.statuses = []
        self.cell = None
        # self.current_action_bar = CurrentActionBar(self.owner)

    # def setup_action(self, action=None):
    #     self.action = action

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

    def dump(self):
        return {
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
            # "action": self.action.__class__.__name__ if self.action else ""
        }
