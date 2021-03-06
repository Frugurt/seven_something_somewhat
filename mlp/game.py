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
            players[0].main_unit.place_in(self._grid[3, 4   ])
            players[-1].main_unit.place_in(self._grid[-1, -1])
        self.winner = None
        for unit in self.units:
            print("STATE", unit.state)
            unit.clear_presumed()
            unit.update_position()
            print(unit._presumed_stats.cell)
            print(unit._stats.cell)
        # self.switch_state()

    @property
    def units(self):
        return self.registry.categories[Unit.__name__]

    def receive_message(self, struct):
        type_pair = tuple(struct['message_type'])
        self.handlers[type_pair](struct['payload'])

    # @staticmethod
    def append_action(self, action_struct):
        # print("APPEND")
        action = action_struct['action']
        author = action_struct['author']
        # print(action.target_coord, action.context['action'].target_coord)
        if author == action.owner.stats.owner or author == "overlord":
            action.owner.append_action(action)
        self.apply_actions()
        # self.update_position()

    # @staticmethod
    def remove_action(self, action_struct):
        unit = action_struct['unit']
        # action_index = action_struct['action_index']
        author = action_struct['author']
        if unit.stats.owner == author or author == "overlord":
            unit.remove_action(None)
        self.clear_presumed()
        # self.apply_actions()
        self.update_position()

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
        result = False
        self.switch_state()
        if all((player.is_ready for player in self.players)):
            anyone_not_pass = self.apply_actions(True)
            for unit in self.turn_order_manager:
                unit.current_action_bar.clear()
            dead_players = {player for player in self.players if player.main_unit.stats.health <= 0}
            alive_players = set(self.players) - dead_players
            if len(alive_players) == 1:
                self.declare_winner(alive_players.pop())
                return
            for unit in self.units:
                unit.launch_triggers("on_phase_start", unit, unit.context)
            if not anyone_not_pass:
                print("all pass")
                self.action_log[-1].append("--------------")
                self.turn_order_manager.rearrange()
                for unit in self.units:
                    unit.refill_action_points()
                    unit.launch_triggers("on_turn_start", unit, unit.context)
            for player in self.players:
                player.is_ready = False
            result = True
            self.clear_presumed()
        self.switch_state()
        return result

    def apply_actions(self, logging=False):
        anyone_not_pass = False
        # print(self.units)
        if logging:
            self.action_log.append([])
        for unit in self.turn_order_manager:
            # print(unit)
            unit_is_not_pass = unit.apply_actions(speed=FAST)
            if logging:
                self.action_log[-1].extend(unit.action_log)
            unit.action_log.clear()
            anyone_not_pass = anyone_not_pass or unit_is_not_pass
        for unit in self.turn_order_manager:
            # print(unit)
            unit_is_not_pass = unit.apply_actions()
            if logging:
                self.action_log[-1].extend(unit.action_log)
            unit.action_log.clear()
            anyone_not_pass = anyone_not_pass or unit_is_not_pass
        for unit in self.turn_order_manager:
            # print(unit)
            unit_is_not_pass = unit.apply_actions(speed=SLOW)
            if logging:
                self.action_log[-1].extend(unit.action_log)
            unit.action_log.clear()
            anyone_not_pass = anyone_not_pass or unit_is_not_pass
        return anyone_not_pass

    def declare_winner(self, player):
        self.winner = player

    def switch_state(self):
        for unit in self.units:
            unit.switch_state()
            # unit.clear_presumed()

    def update_position(self):
        for unit in self.units:
            unit.update_position()

    def clear_presumed(self):
        for unit in self.units:
            unit.clear_presumed()
