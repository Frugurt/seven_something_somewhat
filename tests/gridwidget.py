import sys
sys.path.insert(0, '/home/alessandro/PycharmProjects/mlp')
from tornado import (
    ioloop,
    tcpserver,
    gen,
    queues,
    iostream,
)
import cbor2
from mlp import protocol
from mlp.grid import (
    RectGrid,
    RectCell,
    HexGrid,
    HexCell
)
from mlp.terrain import Grass
from mlp.bind_widget import bind_widget
from mlp.serialization import remote_call
# from mlp.replication_manager import (
#     remote_call,
    # RefDecoder,
# )
import json
from mlp.protocol import *
# from mlp.unit import Muzik


@bind_widget('HexCellWidget')
class GrassCell(HexCell):

    def __init__(self, pos, grid=None):
        super().__init__(pos, grid=grid, terrain=Grass())


@bind_widget('Hexgrid')
class GrassGrid(HexGrid):

    cell = GrassCell


# def decode(message):
#     return cbor2.loads(message, semantic_decoders={40: RefDecoder()})
#
#
# def encode(obj):
#     return cbor2.dumps(obj)

#
# class TestServer(tcpserver.TCPServer):
#
#     def __init__(self, game, *args):
#         self.game = game
#         m = Muzik()
#         m.place_in(self.game.grid[1, 1])
#         super().__init__(*args)
#
#         # self.m = Muzik()
#         # self.stream = None
#         # self.inqueue = queues.Queue()
#         # self.outqueue = queues.Queue()
#
#     @gen.coroutine
#     def handle_stream(self, stream, address):
#         ioloop.IOLoop.current().spawn_callback(self.work_with, stream)
#
#     async def send_update(self, stream):
#         print(self.game.registry.game_objects)
#         print(self.game.registry.dump())
#         payload = self.game.registry.dump()
#         message = {
#             'message_type': (message_type.GAME, game_message.UPDATE),
#             'payload': payload
#         }
#         # await stream.write(json.dumps(message).encode())
#         await stream.write(encode(message))
#
#     async def work_with(self, stream):
#         await self.send_update(stream)
#         while True:
#             try:
#                 msg = await stream.read_bytes(1000, partial=True)
#             except iostream.StreamClosedError:
#                 break
#             else:
#                 message_struct = decode(msg)
#                 print(message_struct)
#                 self.game.receive_message(message_struct)
#                 await self.send_update(stream)


if __name__ == '__main__':
    from kivy.config import Config
    Config.set('graphics', 'width', '810')
    Config.set('graphics', 'height', '810')
    from kivy.app import App
    from kivy.core.image import Image as CoreImage
    from kivy.uix.image import Image
    from kivy.uix.floatlayout import FloatLayout
    from mlp.game import Game
    grid = GrassGrid((8, 8))

    # if sys.argv[1] == 's':
        # server = TestServer(Game(grid))
        # server.listen(1488)
        # ioloop.IOLoop.current().start()
    # else:
    class TestApp(App):

        def build(self):
            wid = FloatLayout()
            # grid_ = grid.make_widget(pos_hint={'x': 0.5, 'y': 0.5})
            # button_ = button.Button(text="MOVE", pos_hint={'x': 0.5, 'y': 0.2}, size_hint=(0.1, 0.1))
            # button_.bind(on_press=lambda _: print(remote_call(m.move)))
            # grid_ = RectGridWidget(grid=grid, pos=(200, 200))
            # grid_ = Muzik().make_widget(pos=(200, 200))
            # grid_ = Image(source='/home/alessandro/PycharmProjects/mlp/man2.png', pos=(200, 200), size=(100,100))
            # wid.add_widget(grid_)
            # wid.add_widget(button_)
            # return grid_
            wid.add_widget(grid.make_widget(pos_hint={'x': 0.1, 'y': 0.1}))
            return wid


    # cells = grid.get_area((4, 4), 1)
    cells = grid.get_ring((4, 4), 2)
    for cell in cells:
        cell.make_widget().is_selected = True

    TestApp().run()
