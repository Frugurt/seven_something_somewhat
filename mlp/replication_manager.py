import random as rnd
from collections import defaultdict
# import json

MAX_OBJECTS = 10**6


class Singleton:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
            cls.instance.init()
        return cls.instance

    def init(self):
        pass


class Registry:

    def __init__(self):
        self.items = {}

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]


class MetaRegistry(Singleton):

    def init(self):
        self.registry = defaultdict(Registry)

    def __getitem__(self, item):
        return self.registry[item]

    def make_registred_meta(self, name):

        class Meta(type):

            registry = self[name]

            def __new__(cls, name, bases, dct):
                # print(bases, dct)
                if 'name' in dct:
                    name = dct['name'] or name
                new_cls = super().__new__(cls, name, bases, dct)
                if bases:
                    cls.registry[name] = new_cls
                # print(new_cls)
                return new_cls
        return Meta


class GameObjectRegistry(Singleton):

    def init(self):
        self.game_objects = {}
        self.game_classes = {}
        self.categories = defaultdict(list)

    def __setitem__(self, key, value):
        if key not in self.game_objects:
            self.game_objects[key] = value
            for cls_name, cls in self.game_classes.items():
                if isinstance(value, cls):
                    self.categories[cls_name].append(value)
        else:
            raise KeyError()

    def __getitem__(self, item):
        return self.game_objects[item]

    def __delitem__(self, key):
        v = self.game_objects.pop(key)
        for category in self.categories.values():
            if v in category:
                category.remove(v)

    def __iter__(self):
        return iter(self.game_objects.values())

    def make_id(self):
        while True:
            id_ = rnd.randint(1, MAX_OBJECTS)
            if id_ not in self.game_objects:
                return id_

    def register_class(self, cls):
        self.game_classes[cls.__name__] = cls

    def dump(self):
        print(list(self.game_objects.items()))
        # return sorted([obj.dump() for id_, obj in self.game_objects.items()], key=lambda x: self.game_classes[x['cls']].load_priority, reverse=True)
        return sorted(
            [obj for id_, obj in self.game_objects.items()], key=lambda x: x.__class__.load_priority, reverse=True
        )

    def load(self, struct):
        pass
        # print(struct)
        # for obj_struct in sorted(struct, key=lambda x: self.game_classes[x['cls']].load_priority, reverse=True):
        #     self.load_obj(obj_struct)
            # id_ = obj_struct['id_']
            # obj = self.game_objects.get(id_)
            # if obj:
            #     obj.load(obj_struct)
            # else:
            #     self.game_classes[obj_struct['cls']](id_=obj_struct.get('id_')).load(obj_struct)

    def load_obj(self, obj_struct):
        id_ = obj_struct['id_']
        obj = self.game_objects.get(id_)
        if obj:
            obj.load(obj_struct)
        else:
            obj = self.game_classes[obj_struct['cls']](id_=obj_struct.get('id_'))
            obj.load(obj_struct)
        return obj

    def purge(self):
        for k in list(self.game_objects.keys()):
            del self[k]

    # def create(self, struct):
    #     for obj_struct in struct:
    #         self.game_classes[obj_struct['cls']](
    #             *obj_struct.get('args'),
    #             id_=obj_struct.get('id_'),
    #             **obj_struct.get('kwargs'),
    #         )

    def remote_call(self, struct):
        struct['method'](*struct['args'], **struct['kwargs'])


class GameObjectMeta(type):

    registry = GameObjectRegistry()

    def __new__(cls, name, bases, dct):
        # print(bases)
        new_cls = super().__new__(cls, name, bases, dct)
        if bases:
            cls.registry.register_class(new_cls)
        # print(new_cls)
        return new_cls


class GameObject(metaclass=GameObjectMeta):
    """
        {
            cls: class_name,
            id: id_ or None
        }
    """

    registry = GameObjectRegistry()
    load_priority = 0
    hooks = []

    def __init__(self, id_=None):
        id_ = id_ or self.registry.make_id()
        self.id_ = id_
        self.registry[id_] = self

    def dump(self):
        return {
            'cls': type(self).__name__,
            'id_': self.id_,
        }

    def load(self, struct):
        pass
