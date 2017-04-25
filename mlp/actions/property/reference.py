from .property import Property


class Reference(Property):

    def __init__(self, name, struct, registry):
        self.name = name
        self.struct = struct
        self.registry = registry

    def get(self, context):
        return self.registry[self.name](**self.struct)
