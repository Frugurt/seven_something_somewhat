from collections import deque
from kivy.uix import (
    floatlayout,
    button,
)
# from mlp.actions.action import (
#     RandomMove,
#     Attack,
# )
# from mlp.serialization import remote_action_setup
from mlp.protocol import *
from ..cursor import MainCursor
from kivy.lang import Builder

# Builder.load_file('/home/alessandro/PycharmProjects/mlp/mlp/widgets/game/game.kv')


class Game(floatlayout.FloatLayout):

    def __init__(self, game, **kwargs):
        self.network_manager = kwargs.pop('network_manager')
        super().__init__(**kwargs)
        # self.network_manager = NetworkManager('localhost', 1488)
        self.game = game
        self.add_widget(game.grid.make_widget(pos_hint={'x': 0.5, 'y': 0.5}))
        button_ = button.Button(
            text="MOVE",
            pos_hint={'x': 0.5, 'y': 0.2},
            size_hint=(0.1, 0.1)
        )
        # button_.bind(on_press=lambda _: self.move_muzik)
        self.add_widget(button_)
        # Clock.schedule_interval(self.watcher, 0)
        # self.network_manager.start()

    # def move_muzik(self, _):
    #     for cell in self.game.grid:
    #         if cell.object is not None:
    #             self.network_manager.send(remote_call(cell.object.move))

    def on_receive_message(self, struct):
        pass

    # def watcher(self, _):
    #     # messages = self.network_manager.dump()
    #     for message in self.network_manager.dump():
    #         message_struct = self.network_manager.decode(message)
    #         print(message_struct)
    #         self.game.receive_message(message_struct)


class RemoteGame(floatlayout.FloatLayout):

    def __init__(self, game, **kwargs):
        self.network_manager = kwargs.pop('network_manager')
        self._cursor = deque([MainCursor(self)])
        super().__init__(**kwargs)
        self.is_loaded = False
        self.grid = None
        self.turn_order_indicator = None
        # self.network_manager = NetworkManager('localhost', 1488)
        self.game = game
        self.stats = None
        self.action_bar = None
        self.current_action_bar = None
        run_button = button.Button(
            text="RUN",
            pos_hint={'x': 0.73, 'y': 0.8},
            size_hint=(0.1, 0.1)
        )
        run_button.bind(on_press=self.run_game)     # TODO внести эту кнопку в главный курсор
        # attack_button = button.Button(
        #     text="Attack",
        #     pos_hint={'x': 0.3, 'y': 0.1},
        #     size_hint=(0.1, 0.1)
        # )
        # attack_button.bind(on_press=self.attack)
        self.add_widget(run_button)
        # self.add_widget(attack_button)
        # Clock.schedule_interval(self.watcher, 0)
        # self.network_manager.start()

    # def move_muzik(self, _):
    #     for cell in self.game.grid:
    #         print(cell.pos, cell.object)
    #         if cell.object is not None:
    #             # print("\n\n\n!!!!\n", cell.object)
    #             self.network_manager.send(remote_call(cell.object.move))

    @property
    def cursor(self):
        return self._cursor[0]

    def add_cursor(self, cursor):
        self.cursor.deactivate()
        self._cursor.appendleft(cursor)
        self.cursor.activate()

    def remove_cursor(self):
        cursor = self._cursor.popleft()
        cursor.deactivate()
        self.cursor.activate()

    # def attack(self, _):
    #     o = self.selected_cell.object
    #     if o is not None:
    #         self.network_manager.send(
    #             remote_action_setup(Attack(o))
    #         )

    def run_game(self, _):
        self.network_manager.send(
            {
                'message_type': (message_type.GAME, game_message.READY),
                # 'payload': {'player': self.parent.app.player_name}
                'payload': {}
            }
        )

    @property
    def selected_cell(self):
        return self.game.grid.make_widget().selected_cell.cell

    def on_receive_message(self, struct):
        # print(struct)
        if not self.is_loaded:
            self.grid = self.game.grid.make_widget(pos_hint={'x': 0.3, 'y': 0.3})
            self.turn_order_indicator = self.game.turn_order_manager.make_widget()
            self.add_widget(self.grid)
            self.add_widget(self.turn_order_indicator)
            # self.grid.update_children()
            # self.grid.bind(selected_cell=self.show_stats)
            self.is_loaded = True
        self.cursor.update()

    def watcher(self, _):
        # messages = self.network_manager.dump()
        for message in self.network_manager.dump():
            message_struct = self.network_manager.decode(message)
            # print(message_struct)
            self.game.receive_message(message_struct)

    # def show_stats(self, _, selected_cell):
    #     if self.stats:
    #         self.remove_widget(self.stats)
    #     if self.action_bar:
    #         self.remove_widget(self.action_bar)
    #     selected_object = selected_cell.cell.object
    #     if selected_object:
    #         # self.stats = selected_object.stats.make_widget(pos_hint={'x': 0.2, 'y': 0.5})
    #         selected_object.make_widget().on_select(self)
    #         # self.add_widget(self.stats)
    #     # else:
    #     #     self.stats = None
