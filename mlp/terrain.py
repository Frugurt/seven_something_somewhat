from .bind_widget import bind_widget


class Terrain:
    pass


@bind_widget('Grass')
class Grass(Terrain):
    hooks = []