from ...tools import convert
from ...replication_manager import MetaRegistry
from collections.abc import Iterable

EFFECTS = MetaRegistry()['Effect']
EffectMeta = MetaRegistry().make_registered_metaclass("Effect")


class AbstractEffect(metaclass=EffectMeta):

    info_message = ""

    def __init__(self, **kwargs):
        self.is_canceled = False

    def log(self, source):
        source.action_log.append(self.info_message)

    def configure(self, **kwargs):
        pass

    def apply(self, *args, **kwargs):
        pass

    def cancel(self):
        self.is_canceled = True

    def __copy__(self):
        pass


class UnitEffect(AbstractEffect):

    # take_event_name = "on_take_" + convert(__name__)
    # after_event_name = "after_take_" + convert(__name__)

    def __init__(self, **kwargs):
        # self.owner = owner
        # self.source = source
        self.info_message = self.info_message
        super().__init__(**kwargs)
        self.take_event_name = "on_take_" + convert(self.__class__.__name__)
        # self.

    def _apply(self, target, source):
        self.log(source)

    def apply(self, cells, source):
        if not isinstance(cells, Iterable):
            cells = [cells]
        for cell in cells:
            if cell.object is not None:
                print("EFFECT EVENT", self.take_event_name)
                cell.object.launch_triggers(self.take_event_name, self, source)
                if not self.is_canceled:
                    self._apply(cell.object, source)
                else:
                    self.is_canceled = False
                    # cell.object.launch_triggers(self.after_event_name, self, source)
        # source_action.owner.action_log.append(self.info_message)

    def copy(self):
        # params = vars(self)
        # params.pop("is_canceled", None)
        # return self.__class__(**params)
        return self.__class__(**vars(self))


class MetaEffect(AbstractEffect):

    def log(self, source):
        source.action_log.append(self.info_message)

    def _apply(self, effect, source, effect_source):
        self.log(source)

    def apply(self, effect, source, effect_source):
        self._apply(effect, source, effect_source)

    def copy(self):
        return self.__class__(**vars(self))


class CustomUnitEffect(UnitEffect):
    pass


def effect_constructor(loader, node):
    e_s = loader.construct_mapping(node)
    name = e_s.pop("name")
    effect = EFFECTS[name](**e_s)
    return effect


def new_effect_constructor(loader, node):
    n_e = loader.construct_mapping(node)
    return

EFFECT_TAG = "!eff"
NEW_EFFECT_TAG = "!new_eff"
