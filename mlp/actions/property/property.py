class Property:

    def get(self, action):
        pass


class Attribute(Property):

    def __init__(self, name):
        self.name = name

    def get(self, action):
        return getattr(action, self.name)

    def __repr__(self):
        return "get {} from action".format(self.name)


class OwnerAttribute(Property):

    def __init__(self, name):
        self.name = name

    def get(self, action):
        return getattr(action.owner, self.name)

    def __repr__(self):
        return "get {} from action owner".format(self.name)


class PresumedCell(Property):

    def get(self, action):
        return action.owner.presumed_cell


PROPERTY_TABLE = {
}


def property_constructor(loader, node):
    property_ = loader.construct_scalar(node)
    if property_ in PROPERTY_TABLE:
        return PROPERTY_TABLE[property_]()
    elif property_.startswith("owner"):
        return OwnerAttribute(property_.split("_", 1)[-1])  # !prop owner_ololo_kuku --> OwnerAttribute("ololo_kuku")
    else:
        return Attribute(property_)

PROPERTY_TAG = "!prop"
