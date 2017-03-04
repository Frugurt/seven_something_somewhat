from itertools import cycle
from .serialization import RefTag
from .replication_manager import (
    GameObjectRegistry,
    GameObject,
)
from random import randint
from .protocol import *
from .bind_widget import bind_widget
from .grid import Grid
from .unit import Unit
from .tools import dict_merge
from .actions.action import (
    SLOW, NORMAL, FAST
)


@bind_widget("TurnOrderIndicator")
class TurnOrderManager(GameObject):

    load_priority = -2
    hooks = ['load']

    def __init__(self, id_=None):
        super().__init__(id_)
        self._current_turn_order = []

    def __iter__(self):
        return iter((x[-1] for x in self._current_turn_order))

    @property
    def units(self):
        return self.registry.categories[Unit.__name__]

    def rearrange(self):
        self._current_turn_order = sorted([
            (
                max((randint(0, 10) for _ in range(u.stats.initiative))),
                u.stats.initiative,
                u,
            )
            for u in self.units
        ], reverse=True)

    def dump(self):
        return dict_merge(
            super().dump(),
            {'current_turn_order': list(enumerate((RefTag(u) for u in self)))},
        )
        # return {
        #     **super().dump(),
        #     'current_turn_order': list(enumerate((RefTag(u) for u in self)))
        # }

    def load(self, struct):
        super().load(struct)
        self._current_turn_order = sorted(struct['current_turn_order'])


@bind_widget('RemoteGame')
class Game:

    hooks = ['receive_message']

    def __init__(self, players=None, grid=None, turn_order_manager=None):
        self.registry = GameObjectRegistry()
        self.action_log = []
        self.handlers = {
            (message_type.GAME, game_message.CALL): self.registry.remote_call,
            (message_type.GAME, game_message.UPDATE): self.registry.load,
            (message_type.GAME, game_message.ACTION_APPEND): self.append_action,
            (message_type.GAME, game_message.ACTION_REMOVE): self.remove_action,
            # (message_type.GAME, game_message.READY): self.run,
        }
        self._grid = grid
        self._turn_order_manager = turn_order_manager
        self.players = players
        if players:
            players[0].main_unit.place_in(self._grid[3, 3])
            players[-1].main_unit.place_in(self._grid[-1, -1])
        self.winner = None

    def receive_message(self, struct):
        type_pair = tuple(struct['message_type'])
        self.handlers[type_pair](struct['payload'])

    @staticmethod
    def append_action(action_struct):
        action = action_struct['action']
        author = action_struct['author']
        if author == action.owner.stats.owner or author == "overlord":
            action.owner.append_action(action)

    @staticmethod
    def remove_action(action_struct):
        unit = action_struct['unit']
        # action_index = action_struct['action_index']
        author = action_struct['author']
        if unit.stats.owner == author or author == "overlord":
            unit.remove_action(None)

    @property
    def units(self):
        return self.registry.categories[Unit.__name__]

    @property
    def grid(self):
        if self._grid is None:
            for o in self.registry:
                if isinstance(o, Grid):
                    self._grid = o
                    break
        return self._grid

    @property
    def turn_order_manager(self):
        if self._turn_order_manager is None:
            for o in self.registry:
                if isinstance(o, TurnOrderManager):
                    self._turn_order_manager = o
                    break
        return self._turn_order_manager

    def run(self):
        if all((player.is_ready for player in self.players)):
            self.action_log.append([])
            anyone_not_pass = False
            # print(self.units)
            for unit in self.turn_order_manager:
                # print(unit)
                unit_is_not_pass = unit.apply_actions(speed=FAST)
                self.action_log[-1].extend(unit.action_log)
                unit.action_log.clear()
                anyone_not_pass = anyone_not_pass or unit_is_not_pass
            for unit in self.turn_order_manager:
                # print(unit)
                unit_is_not_pass = unit.apply_actions()
                self.action_log[-1].extend(unit.action_log)
                unit.action_log.clear()
                anyone_not_pass = anyone_not_pass or unit_is_not_pass
            for unit in self.turn_order_manager:
                # print(unit)
                unit_is_not_pass = unit.apply_actions(speed=SLOW)
                self.action_log[-1].extend(unit.action_log)
                unit.action_log.clear()
                anyone_not_pass = anyone_not_pass or unit_is_not_pass
            for unit in self.turn_order_manager:
                unit.current_action_bar.clear()
                unit.clear_preparations()
            dead_players = {player for player in self.players if player.main_unit.stats.health <= 0}
            alive_players = set(self.players) - dead_players
            if len(alive_players) == 1:
                self.declare_winner(alive_players.pop())
                return
            if not anyone_not_pass:
                print("all pass")
                self.action_log[-1].append("--------------")
                self.turn_order_manager.rearrange()
                for unit in self.units:
                    unit.refill_action_points()
            for player in self.players:
                player.is_ready = False
            return True
        return False

    def declare_winner(self, player):
        self.winner = player
