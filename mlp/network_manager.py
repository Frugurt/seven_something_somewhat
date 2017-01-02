from threading import Thread
import queue
# from .replication_manager import RefDecoder
from collections import deque
from tornado import (
    ioloop,
    gen,
    queues as tq,
    tcpclient,
    iostream
)
from .serialization import (
    mlp_dumps,
    mlp_loads,
)
# from collections import deque
# from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.boxlayout import BoxLayout
# from kivy.clock import Clock


class NetworkManager(Thread):

    def __init__(self, host=None, port=None, encoder=mlp_dumps, decoder=mlp_loads):
        super().__init__(name="NetworkManager")
        self.loop = ioloop.IOLoop.current()
        self.client = tcpclient.TCPClient()
        self.inqueue = tq.Queue()
        self.outqueue = queue.Queue()
        self.encode = encoder
        self.decode = decoder

        self.host = host
        self.port = port

    @gen.coroutine
    def connect(self):
    # async def connect(self):
        host, port = self.host, self.port
        # stream = await self.client.connect(host, port)
        stream = yield self.client.connect(host, port)
        # stream.set_nodelay(True)
        self.loop.spawn_callback(self.consumer, stream)
        self.loop.spawn_callback(self.receiver, stream)


    @gen.coroutine
    def consumer(self, stream):
    # async def consumer(self, stream):
        while True:
            # text = await self.inqueue.get()
            text = yield self.inqueue.get()
            print("bytes sended", text)
            # await stream.write(text)
            yield stream.write(text + b"|||")


    @gen.coroutine
    def receiver(self, stream):
    # async def receiver(self, stream):
        while True:
            try:
                # text = await stream.read_bytes(10000, partial=True)
                # text = yield stream.read_bytes(100000, partial=True)
                text = yield stream.read_until(b"|||")
                text = text.rstrip(b"|||")
                # status = stream.get_fd_error()
                # if status:
                #     print(str(status))
                print("bytes recieved", text)
            except iostream.StreamClosedError:
                break
            else:
                self.outqueue.put_nowait(text)

    def send(self, struct):
        # print('send', struct)
        message = self.encode(struct)
        self.inqueue.put_nowait(message)

    def dump(self):
        data = deque()
        while not self.outqueue.empty():
            data.append(self.outqueue.get_nowait())
        return data

    def run(self):
        self.loop.spawn_callback(self.connect)
        self.loop.start()
