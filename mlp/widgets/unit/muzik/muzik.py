# from kivy.core.image import Image as CoreImage
# texture = CoreImage('/home/alessandro/PycharmProjects/mlp/grass.png')
from mlp.widgets.unit.unit import Unit


class Muzik(Unit):

    def __init__(self, muzik, **kwargs):
        super().__init__(muzik, source='./data/duelist.png', **kwargs)
        # super().__init__(muzik, source='/home/alessandro/PycharmProjects/mlp/man2.png', size=(128, 128), **kwargs)
