from kivy.core.image import Image as CoreImage
from ..terrain import Terrain
texture = CoreImage('./data/grass.png')


class Grass(Terrain):
    texture = texture
