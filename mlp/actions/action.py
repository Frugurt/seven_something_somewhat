# from ..replication_manager import (
#     ActionsRegistry,
#     ActionMeta,
# )
from ..serialization import RefTag, ActionTag
from ..bind_widget import bind_widget
from ..tools import dict_merge

FULL, MOVE, STANDARD = range(3)
FAST, NORMAL, SLOW = range(3)


@bind_widget("ActionBar")
class ActionBar:

    hooks = []

    def __init__(self, owner, actions):
        self.owner = owner
        self.actions = [
            action(owner) for action in actions
        ]


@bind_widget("CurrentActionBar")
class CurrentActionBar:

    hooks = ['append_action', 'remove_action']

    def __init__(self, owner):
        self.owner = owner
        self.actions = []
        self.preparations = []

    def append_action(self, action):
        # if self.check_slots(action) and action.pre_check() and action.post_check():
        if self.check_slots(action) and action.check():
            self.actions.append(action)
            # action.append_to_bar_effect()

    def remove_action(self, action_index):
        self.actions.clear()
        # try:
        #     action = self.actions.pop(action_index)
        # except IndexError:
        #     action = self.actions.pop(0)
        # finally:
        # action.remove_from_bar_effect()

    def check_slots(self, action):
        action_type = action.action_type
        actions = self.actions
        l = len(actions)
        if l >= 2:
            print("NO TOMANY")
            return False
        elif l == 1:
            l_a_t = actions[-1].action_type
            if l_a_t == FULL:
                print("NO FULL")
                return False
            elif (
                    l_a_t == STANDARD and action_type == MOVE or
                    l_a_t == MOVE and action_type != FULL
            ):
                return True
            else:
                print("NO", action, actions)
                return False
        else:
            return True

    def apply_actions(self, speed=NORMAL):
        any_action = bool(self.actions)
        for action in (action for action in self.actions if action.action_speed == speed):
            if action.pre_check():
                action.apply()
        # self.clear()
        return any_action

    def clear(self):
        for i in range(len(self.actions)):
            self.remove_action(0)

    def clear_preparations(self):
        self.preparations.clear()

    def dump(self):
        return [ActionTag(action) for action in self.actions]

    def load(self, struct):
        self.clear()
        for action in struct:
            self.append_action(action)

    def __iter__(self):
        return iter(self.actions)


# class Action(metaclass=ActionMeta):
#     hooks = []
#     action_type = None
#     action_speed = NORMAL
#     move_points_cost = 0
#     action_points_cost = 0
#
#     def __init__(self, target):
#         self.target = target
#
#     def setup(self):
#         pass
#
#     def clear(self):
#         pass
#
#     def apply(self):
#         self.target.stats.move_points -= self.move_points_cost
#         self.target.stats.action_points -= self.action_points_cost
#
#     def dump(self):
#         return {
#             'name': self.__class__.__name__,
#             'target': RefTag(self.target),
#         }
#
#     def pre_check(self):
#         enough_action_points = self.target.stats.action_points >= self.action_points_cost
#         enough_move_points = self.target.stats.move_points >= self.move_points_cost
#         return enough_action_points and enough_move_points
#
#     def post_check(self):
#         return True
#
#     def append_to_bar_effect(self):
#         pass
#
#     def remove_from_bar_effect(self):
#         pass


# @bind_widget('RandomMove')
# class Move(Action):
#
#     action_type = MOVE
#     move_points_cost = 1
#
#     def __init__(self, target, target_coord=None, move_index=None):
#         super().__init__(target)
#         self.target_coord = target_coord
#         self.move_index = move_index
#
#     def setup(self):
#         target_cell = yield "adjacent_cell", (self.target.presumed_cell,)
#         self.target_coord = target_cell.pos
#
#     def clear(self):
#         self.target_coord = None
#
#     def apply(self):
#         super().apply()
#         if self.target_coord is not None:
#             self.target.pos = self.target_coord
#             self.target.action_log.append(
#                 "{} move to {}".format(self.target, self.target_coord)
#             )
#
#     def dump(self):
#         return dict_merge(
#             super().dump(),
#             {
#                 # **super().dump(),
#                 'target_coord': self.target_coord,
#                 'move_index': self.move_index
#             }
#         )
#
#     def append_to_bar_effect(self):
#         assert self.target_coord is not None
#         self.move_index = self.target.append_to_path(self.target_coord)
#
#     def remove_from_bar_effect(self):
#         assert self.move_index is not None
#         self.target.remove_from_path(self.move_index)


# @bind_widget('Attack')
# class Attack(Action):
#
#     action_type = STANDARD
#     action_points_cost = 1
#
#     def pre_check(self):
#         return super().pre_check()
#
#     def apply(self):
#         super().apply()
#         if self.target.stats.unit_state == "sword":
#             self.target.action_log.append(
#                 str(self.target) + "swing with sword"
#             )
#             for c in self.target.cell.adjacent:
#                 if c.object is not None:
#                     self.target.action_log.append(
#                         "and hit {}".format(c.object)
#                     )
#                     if "parry" in c.object.current_action_bar.preparations:
#                         self.target.stats.take_damage(self.target.stats.attack)
#                         self.target.action_log.append(
#                             "but fucked with parry and take {} damage".format(self.target.stats.attack)
#                         )
#                     else:
#                         c.object.stats.take_damage(self.target.stats.attack)
#                         self.target.action_log.append(
#                             "{} take {} damage".format(c.object, self.target.stats.attack)
#                         )
#
#
# @bind_widget('Shoot')
# class Shoot(Action):
#
#     action_type = STANDARD
#     action_points_cost = 1
#     action_speed = SLOW
#
#     def __init__(self, target, line=None):
#         super().__init__(target)
#         self.line = line
#
#     def setup(self):
#         line = yield "line", (self.target.presumed_cell,)
#         self.line = [cell.pos for cell in line]
#
#     def clear(self):
#         self.line = None
#
#     def dump(self):
#         return dict_merge(
#             super().dump(),
#             {
#                 # **super().dump(),
#                 'line': self.line
#             }
#     )
#
#     def apply(self):
#         super().apply()
#         if self.target.stats.unit_state == "rifle":
#             self.target.action_log.append(
#                 "{} shoot".format(self.target)
#             )
#             self.target.stats.loaded = False
#             grid = self.target.cell.grid
#             for pos in self.line:
#                 self.target.action_log.append(
#                     "bullet fly through {}".format(pos)
#                 )
#                 cell = grid[pos]
#                 if cell.object is not None and cell.object.id_ != self.target.id_:
#                     self.target.action_log.append(
#                         "and hit {}".format(cell.object)
#                     )
#                     cell.object.stats.take_damage(35)
#                     self.target.action_log.append(
#                         "{} take {} damage".format(cell.object, 35)
#                     )
#                     break
#
#     def pre_check(self):
#         return super().pre_check() and self.target.stats.loaded
#
#
# @bind_widget("ChangeWeapon")
# class ChangeWeapon(Action):
#
#     action_type = MOVE
#     move_points_cost = 1
#
#     def apply(self):
#         super().apply()
#         if self.target.stats.unit_state == "sword":
#             self.target.action_log.append(
#                 "{} now with rifle".format(self.target)
#             )
#             self.target.stats.unit_state = "rifle"
#         else:
#             self.target.action_log.append(
#                 "{} now with sword".format(self.target)
#             )
#             self.target.stats.unit_state = "sword"
#
#
# @bind_widget("Reload")
# class Reload(Action):
#
#     action_type = FULL
#     action_points_cost = 1
#     move_points_cost = 1
#
#     def apply(self):
#         super().apply()
#         self.target.action_log.append(
#             "{} now loaded".format(self.target)
#         )
#         self.target.stats.ammo -= 1
#         self.target.stats.loaded = True
#
#     def pre_check(self):
#         return super().pre_check() and self.target.stats.ammo > 0 and self.target.stats.unit_state == "rifle"
#
#
# @bind_widget("Parry")
# class Parry(Action):
#
#     action_type = FULL
#     action_points_cost = 1
#     move_points_cost = 1
#     action_speed = FAST
#
#     def pre_check(self):
#         return super().pre_check() and self.target.stats.unit_state == "sword" and not self.target.stats.parried
#
#     def apply(self):
#         super().apply()
#         self.target.action_log.append(
#             "{} parry".format(self.target)
#         )
#         self.target.current_action_bar.preparations.append('parry')
#         self.target.stats.parried = True

    # def append_to_bar_effect(self):
    #     self.target.current_action_bar.preparations.append('parry')
    #
    # def remove_from_bar_effect(self):
    #     try:
    #         self.target.current_action_bar.preparations.remove('parry')
    #     except ValueError:
    #         pass
