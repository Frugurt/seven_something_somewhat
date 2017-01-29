import yaml
from ..replication_manager import (
    ActionsRegistry,
    ActionMeta,
)
from ..protocol import Enum
from .effect import EFFECTS

# from ..serialization import RefTag, ActionTag
# class Namespace:
#
#     def __init__(self, **consts):
#         for const_name, const_val in consts.items():
#             setattr(self, const_name, const_val)
#
#     def __repr__(self):
#         return "\n".join(map(lambda name_val: "{0} = {1}".format(name_val[0], name_val[1]), self.items()))
#
#     def values(self):
#         return self.__dict__.itervalues()
#
#     def names(self):
#         return self.__dict__.iterkeys()
#
#     def items(self):
#         return self.__dict__.items()
#
#
# class Enum(Namespace):
#     def __init__(self, *consts):
#         for const_name, const_val in zip(consts, range(len(consts))):
#             setattr(self, const_name, const_val)

FULL, MOVE, STANDARD = range(3)
type_ = Enum(
    "FULL",
    "MOVE",
    "STANDARD",
)
# FAST, NORMAL, SLOW = range(3)
speed = Enum(
    "FAST",
    "NORMAL",
    "SLOW",
)


class Property:

    def get(self, action):
        pass


class Attribute(Property):

    def __init__(self, name):
        self.name = name

    def get(self, action):
        return getattr(action, self.name)

    def __repr__(self):
        return "get {} from action".format(self.name)


class Area(Property):
    pass


class OwnerCell(Area):

    def get(self, action):
        return action.owner.cell

    def __repr__(self):
        return "get action owner cell"


PROPERTY_TABLE = {
    'owner_cell': OwnerCell
}


# class Action(metaclass=ActionMeta):
class Action:
    hooks = []

    name = None
    cost = 0
    action_type = None
    action_speed = None

    setup_fields = []
    effects = []
    area = None

    widget = None

    def __init__(self, owner):
        self.owner = owner
        for setup_struct in self.setup_fields:
            field_name = setup_struct['name']
            setattr(self, field_name, None)
        self.effects = [effect.copy() for effect in self.effects]

    def setup(self):
        for setup_struct in self.setup_fields:
            cursor_params = [
                p.get(self) if isinstance(p, Property) else p
                for p in setup_struct['cursor_params']
            ]
            value = yield [setup_struct['cursor']] + cursor_params
            setattr(self, setup_struct['name'], value)

    def clear(self):
        for setup_struct in self.setup_fields:
            field_name = setup_struct['name']
            setattr(self, field_name, None)

    def apply(self):
        cells = self.area.get(self)
        for effect in self.effects:
            effect.apply(cells)

    def pre_check(self):
        pass

    def post_check(self):
        pass


def property_constructor(loader, node):
    property_ = loader.construct_scalar(node)
    if property_ in PROPERTY_TABLE:
        return PROPERTY_TABLE[property_]()
    else:
        return Attribute(property_)

yaml.add_constructor("!prop", property_constructor)

ACTIONS_TABLE = {}


def actions_constructor(loader, node):
    a_s = loader.construct_mapping(node)

    class NewAction(Action):
        name = a_s['name']
        action_type = getattr(type_, a_s['action_type'])
        action_speed = getattr(speed, a_s['speed'])
        cost = a_s['cost']
        setup_fields = a_s['setup']
        area = a_s['area']
        effects = a_s['effects']
        widget = a_s['widget']

    return NewAction

yaml.add_constructor("!new_action", actions_constructor)


def effect_constructor(loader, node):
    e_s = loader.construct_mapping(node)
    name = e_s.pop("name")
    effect = EFFECTS[name](**e_s)
    return effect

yaml.add_constructor("!eff", effect_constructor)

if __name__ == '__main__':
    with open('./mlp/actions/actions.yaml') as a:
        c = yaml.load(a)
