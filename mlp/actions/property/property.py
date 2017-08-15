"""
context - это словарь в котором могут быть такие параметры

target -> то к чему применяется эффект
owner -> тот кто использует действие применяющее эффект
action -> действие накладывающее эффект
source -> клетка из которой было совершено действие

У мета эффектов
effect_context -> контекст эффекта на который применяется метаэффект
"""


class Property:

    def get(self, context):
        pass


class Attribute(Property):

    def __init__(self, path):
        path = path.split(".")
        self.donor = path[0]
        self.path = path[1::]
        print("ATTR", self.donor, self.path)

    def get(self, context):
        print(context, self.donor, self.path)
        donor = context[self.donor]
        for p in self.path:
            donor = getattr(donor, p)
        return donor

    def __repr__(self):
        return "get {} from {}".format(
            ".".join(self.path),
            self.path[0],
        )


class UnitAttribute(Attribute):

    def __init__(self, path):
        path = path.split(".")
        self.donor = path[0]
        self.path = ["stats"] + path[1::]


# class PresumedCell(Property):
#
#     def get(self, context):
#         return context.owner.presumed_cell


class Const(Property):

    def __init__(self, v):
        self.v = v

    def get(self, context):
        return self.v


class Oper(Property):

    def __init__(self, oper, left, right):
        self.oper = oper
        self.left = left
        self.right = right

    def get(self, context):
        left = self.left.get(context)
        right = self.right.get(context)
        print(left, self.left)
        print(right, self.right)
        return self.oper(self.left.get(context), self.right.get(context))


PROPERTY_TABLE = {
}


def property_constructor(loader, node):
    property_ = loader.construct_scalar(node)
    if property_ in PROPERTY_TABLE:
        return PROPERTY_TABLE[property_]()
    elif property_.startswith("owner") or property_.startswith("target"):
        return UnitAttribute(property_)
    else:
        return Attribute(property_)

PROPERTY_TAG = "!prop"
