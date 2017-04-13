from ...tools import (
    convert,
    dotdict,
)
from ..property.property import (
    Property,
    # Const,
)
from ...replication_manager import MetaRegistry
from collections.abc import Iterable
from contextlib import contextmanager

EFFECTS = MetaRegistry()['Effect']
EffectMeta = MetaRegistry().make_registered_metaclass("Effect")


class AbstractEffect(metaclass=EffectMeta):

    info_message = ""
    name = ""

    def __init__(self, **kwargs):
        self.is_canceled = False

    def log(self, source):
        source.action_log.append(self.info_message)

    @contextmanager
    def configure(self, context):
        context_values = dotdict()
        # print("CONFIGURE", vars(self))
        for k, v in vars(self).items():
            if isinstance(v, Property):
                context_values[k] = v.get(context)
            else:
                context_values[k] = v
        yield context_values

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
        self.take_event_name = "on_take_" + convert(self.name or self.__class__.__name__)
        # self.

    def _apply(self, target, context):
        source = context['source']
        # self.configure(context)
        self.log(source)

    def apply(self, cells, context):
        if not isinstance(cells, Iterable):
            cells = [cells]
        for cell in cells:
            if cell.object is not None:
                effect_context = context.copy()
                effect_context['target'] = cell.object
                # print("EFFECT EVENT", self.take_event_name)
                cell.object.launch_triggers(self.take_event_name, self, effect_context)
                if not self.is_canceled:
                    self._apply(cell.object, effect_context)
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

    def _apply(self, effect, context, effect_context):
        self.log(context)

    def apply(self, effect, context, effect_context):
        self._apply(effect, context, effect_context)

    def copy(self):
        return self.__class__(**vars(self))


class CustomUnitEffect(UnitEffect):

    name = None
    params = []
    effects = []

    def __init__(self, **kwargs):
        # assert set(self.params) == set(kwargs.keys())
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def apply(self, cells, context):
        context['effect'] = self
        super().apply(cells, context)

    def _apply(self, target, context):
        for e_s in self.effects:
            cond = e_s.get('condition')
            if cond is None or cond.get(context):
                effect = e_s['effect']
                effect._apply(target, context)     # TODO перепроектировать это


def effect_constructor(loader, node):
    e_s = loader.construct_mapping(node)
    name = e_s.pop("name")
    effect = EFFECTS[name](**e_s)
    return effect


def new_effect_constructor(loader, node):
    n_e = loader.construct_mapping(node)

    class NewEffect(CustomUnitEffect):
        name = n_e["name"]
        effects = n_e['effects']
        params = n_e['params']

    return NewEffect

EFFECT_TAG = "!eff"
NEW_EFFECT_TAG = "!new_eff"
