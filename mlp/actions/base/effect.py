from ...tools import convert
from collections.abc import Iterable


class AbstractEffect:

    info_message = ""

    def log(self, source):
        source.action_log.append(self.info_message)

    def configure(self, **kwargs):
        pass

    def apply(self, *args, **kwargs):
        pass

    def __copy__(self):
        pass


class UnitEffect(AbstractEffect):

    def __init__(self, **kwargs):
        # self.owner = owner
        # self.source = source
        self.info_message = self.info_message
        self.take_event_name = "on_take_" + convert(self.__class__.__name__)

    def _apply(self, target, source):
        self.log(source)

    def apply(self, cells, source):
        if not isinstance(cells, Iterable):
            cells = [cells]
        for cell in cells:
            if cell.object is not None:
                cell.object.launch_triggers(self.take_event_name, self, source)
                self._apply(cell.object, source)
        # source_action.owner.action_log.append(self.info_message)

    def copy(self):
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

EFFECTS = {}
