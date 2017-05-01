from itertools import (
    chain,
    combinations,
)
from mlp.replication_manager import (
    GameObject,
    # RefTag,
    # ActionsRegistry,
    MetaRegistry,
)
# from mlp.bind_widget import bind_widget
# from mlp.stats import (
#     Stats,
#     MajorStats,
# )
from mlp.stats.new_stats import MajorStats
from mlp.grid import Grid
from mlp.actions.action import *
from mlp.actions.new_action import *
from mlp.tools import dict_merge

PLANNING, ACTION = range(2)


class Unit(GameObject):

    hooks = []
    actions = []
    resources = {}

    def __init__(self, master_name=None, id_=None):
        super().__init__(id_)
        self._last_cell = None
        self.state = PLANNING
        self.presumed_path = []
        self.action_log = []
        self._stats = MajorStats(self.__class__.__name__, master_name, self.resources)
        self.current_action_bar = CurrentActionBar(self)
        registry = MetaRegistry()["Action"]
        self.action_bar = ActionBar(
            self,
            [registry[action_name] for action_name in self.actions],
        )
        self.clear_presumed()
        self.context = {'source': self}

    @property
    def _presumed_stats(self):
        return self._stats.presumed

    @property
    def presumed_cell(self):
        """
        Сейчас это просто последняя клетка. Если отталкиваться от идеи, что в случае если клетка недостижима из текушщей
        но достижима в принципе, то чувачок ищет путь до неё и идёт туда, то предполагаемая клетка должна высчитыватсья
        примерно так:
        1) Исходная предполагаемая клетка - наша клетка
        2) Есть ли клетка в предполагаемом пути?
        3) Если нет - заканчиваем. Если да достижима ли она?
        4) Если нет - заканчиваем. Если да, то достижима ли она из текущей предполагаемой клетки
        5) Если да, то новая предполагаемая клетка - наша клетка. Если нет - строим путь и берём ближайшую.
        :return:
        """
        # pos = reduce(lambda prev, cur: (prev[0] + cur[1][0], prev[1] + cur[1][1]), self.presumed_path, self.pos)
        # if self.presumed_path:
        #     return self.cell.grid[self.presumed_path[-1][-1]]
        # else:
        return self.cell

    @property
    def real_cell(self):
        return self._stats.cell

    @property
    def stats(self):
        if self.state == ACTION:
            return self._stats
        else:
            return self._presumed_stats
            # return self._stats.presumed

    @property
    def cell(self):
        # try:
        return self.stats.cell
        # except AttributeError:

    @cell.setter
    def cell(self, cell):
        self.stats.cell = cell

    def place_in(self, cell):
        """
        Указать, что юнит на самом деле в этой клетке
        :param cell:
        :return:
        """
        # self.pos = cell.pos
        # if self.cell:
        #     self.cell.take(self)
        # self.cell = cell
        # if self.state == ACTION:
        # cell.place(self)
        self._stats.cell = cell
        # self.update_position()

    def update_position(self):
        """
        Поместить юнит в нужную клетку
        :return:
        """
        print("Update")
        print(self._presumed_stats.cell)
        print(self._stats.cell)
        if self.cell:
            if self._last_cell:
                self._last_cell.take(self)
            self._last_cell = self.cell
            self.cell.place(self)

    def move(self, cell):
        """
        Передвинуть юнит
        :param cell:
        :return:
        """
        if self.state == PLANNING:
            self._presumed_stats.cell = cell
        else:
            self._stats.cell = cell
            self.update_position()
        # target_cell = choice(self.cell.adjacent)
        # self.place_in(cell)

    def dump(self):
        return dict_merge(
            super().dump(),
            {
                # 'pos': self.pos,
                'stats': self._stats.dump(),
                # 'presumed_stats': self._presumed_stats.dump(),
                'current_actions': self.current_action_bar.dump(),
            }
        )

    def load(self, struct):
        # self.pos = struct['pos']
        self._stats.load(struct['stats'])
        # self._presumed_stats.load(struct['presumed_stats'])
        self.current_action_bar.load(struct['current_actions'])
        self.update_position()
        # if self._stats.cell:
        #     self.pos = self._stats.cell.pos
        # self.master_name = struct['master_name']

    @property
    def pos(self):
        try:
            return self.cell.pos
        except AttributeError:
            return None

    @pos.setter
    def pos(self, pos):
        if pos is None:
            return
        try:
            self.place_in(self.cell.grid[pos])
        except AttributeError:
            for obj in self.registry:
                print(obj)
                if isinstance(obj, Grid):
                    self.place_in(obj[pos])

    def append_action(self, action):
        self.current_action_bar.append_action(action)
        # self.stats.setup_action(action)

    def remove_action(self, action_index):
        self.current_action_bar.remove_action(action_index)

    def apply_actions(self, speed=SPEED.NORMAL):
        return self.current_action_bar.apply_actions(speed)

    def refill_action_points(self):
        self.stats.action_points = 3       # TODO сделать по людски
        self.stats.move_points = 3
        for status in list(self.stats.statuses.values()):
            status.tick()

    def clear_presumed(self):
        self._stats.update_presumed()

    def __repr__(self):
        who = "{} {} at".format(self.stats.owner, self.__class__.__name__)
        where = "{}".format(self.stats.cell)
        return " ".join((who, where))

    # def __cmp__(self, other):
    #     return 1 if id(self) > id(other) else (-1 if id(self) < id(other) else 0)

    def __eq__(self, other):
        return id(self) == id(other)

    def __lt__(self, other):
        return id(self) < id(other)

    def switch_state(self):
        # self.stats.switch_state()
        # self.cell.take(self)
        self.state = int(not self.state)
        # self.place_in(self.cell)
        self.update_position()
        # self.cell.place(self)
        if self.state:
            print("NOW IN ACTION")
        else:
            print("NOW IN PLANNING")

    def add_status(self, status):
        self.stats.statuses[status.name] = status
        for event in status.events:
            self.stats.triggers[event][status.name] = status
        status.on_add(self)
        # print("STATUS", self.state, self.stats.statuses)

    def remove_status(self, status):
        # traceback.print_stack()
        # i = self.stats.statuses.index(status)
        # print("PLANNING STATUSES", self._presumed_stats.statuses)
        # print("ACTION STATUSES", self._stats.statuses)
        s = self.stats.statuses.pop(status.name)
        for event in status.events:
            self.stats.triggers[event].pop(status.name)
        s.on_remove(self)

    # def add_trigger(self, trigger):
    #     for event in trigger.events:
    #         self.stats.triggers[event][trigger.name] = trigger

    # def remove_trigger(self, trigger):
    #     for event in trigger.events:
    #         self.stats.triggers[event].pop(trigger.name)

    def launch_triggers(self, tags, target, target_context):
        print("\n\n\n\nLaunch")
        print(tags)
        l = len(tags)
        for event in chain(*(combinations(tags, j) for j in range(1, l+1))):
            event = frozenset(event)
            for trigger in list(self.stats.triggers[event].values()):
                trigger.apply(event, target, target_context)


def unit_constructor(loader, node):
    u_s = loader.construct_mapping(node)

    print("LOAD", u_s['name'])

    @bind_widget('Unit')
    class NewUnit(Unit):
        name = u_s['name']
        actions = u_s['actions']
        widget = u_s['widget']
        resources = u_s['resources']

    NewUnit.__name__ = NewUnit.name
    return NewUnit

NEW_UNIT_TAG = "!new_unit"
