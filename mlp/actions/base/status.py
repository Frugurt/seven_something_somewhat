from ...replication_manager import MetaRegistry


STATUSES = MetaRegistry()["Status"]
StatusMeta = MetaRegistry().make_registered_metaclass("Status")


class Status(metaclass=StatusMeta):

    name = None

    def __init__(self, context=None, **kwargs):
        # pass
        self.context = context

    def configure(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def on_add(self, target):
        pass

    def on_remove(self, target):
        pass

    def dump(self):
        return {
            "name": self.name,
            "context": self.context,
        }

    def __repr__(self):
        return "Status {}".format(self.name)

    def copy(self):
        return self.__class__(**vars(self))


class CustomStatus(Status):

    on_add_effects = []
    on_remove_effects = []

    def on_add(self, target):
        for effect in self.on_add_effects:
            effect.apply(target.stats.cell, self.context)
            # TODO переписать эффекты, чтобы можно было просто передать цель

    def on_remove(self, target):
        for effect in self.on_remove_effects:
            effect.apply(target.stats.cell, self.context)


def status_constructor(loader, node):
    s_s = loader.construct_mapping(node)
    name = s_s.pop("name")
    status = STATUSES[name](**s_s)
    return status

STATUS_TAG = "!status"


def new_status_constructor(loader, node):
    s_s = loader.construct_mapping(node)

    class NewStatus(CustomStatus):

        name = s_s.pop("name")
        on_add_effects = s_s.pop("on_add")
        on_remove_effects = s_s.pop("on_remove")

    return NewStatus

NEW_STATUS_TAG = "!new_status"
