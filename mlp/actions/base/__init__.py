from collections.abc import Iterable
from .effect import (
    UnitEffect,
    MetaEffect,
    EFFECTS,
)
from .status import (
    Status,
    STATUSES,
)


class Move(UnitEffect):

    info_message = "{} move to {}"

    def __init__(self, **kwargs):
        self.path = kwargs['path']
        # print("TARGET COORD", self.target_coord)
        super().__init__(**kwargs)

    # def _apply(self, source_action, target):

    def _apply(self, target, context):
        # print("CONTEXT", context['action'].target_coord)
        with self.configure(context) as c:
            path = c.path
            grid = target.cell.grid
            if not isinstance(path, Iterable):
                path = [path]
            for path_part in path:
                next_cell = grid.find_path(target.cell, path_part)[1]
                if next_cell.object is None:
                    target.move(next_cell)
            self.info_message = self.info_message.format(target, c.path)
            super()._apply(target, context)


class Damage(UnitEffect):

    name = "Damage"
    info_message = "{} take {} damage"
    _tags = ['harmful', 'damage']

    def __init__(self, amount, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount

    def _apply(self, target, context):
        with self.configure(context) as c:
            target.stats.health -= c.amount
            self.info_message = self.info_message.format(target, c.amount)
            super()._apply(target, context)
            
class Heal(UnitEffect):

    info_message = "{} restore {} health"

    def __init__(self, amount, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount

    def _apply(self, target, context):
        with self.configure(context) as c:
            target.stats.health += c.amount
            self.info_message = self.info_message.format(target, c.amount)
            super()._apply(target, context)


class AddStatus(UnitEffect):

    info_message = "add {} to {}"

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        self.status = status

    def _apply(self, target, context):
        # if cell.object:
        with self.configure(context) as c:
            status = c.status.configure(context=context)
            target.add_status(status)
            self.info_message = self.info_message.format(c.status, target)
            super()._apply(target, context)


class RemoveStatus(UnitEffect):

    info_message = "remove {} from {}"

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        self.status = status

    def _apply(self, target, context):
        # if cell.object:
        with self.configure(context) as c:
            target.remove_status(c.status)
            self.info_message = self.info_message.format(c.status, target)
            # print(self.info_message)
            super()._apply(target, context)


class ChangeStat(UnitEffect):

    info_message = "change stat {} of {} to {}"

    def __init__(self, stat_name, value=None, **kwargs):
        self.stat_name = stat_name
        self.value = value
        super().__init__(stat_name=stat_name, value=value, **kwargs)

    # def configure(self, stat_name=None, value=None):
    #     self.value = value or self.value
    #     self.stat_name = stat_name or self.stat_name

    def _apply(self, target, context):
        with self.configure(context) as c:
            self.info_message = self.info_message.format(
                c.stat_name,
                target,
                c.value,
            )
            setattr(target.stats, c.stat_name, c.value)
            super()._apply(target, context)


class Reflect(MetaEffect):

    info_message = "reflect {} to {}"

    def _apply(self, effect, context, effect_context):
        print(context, "context")
        print(effect_context, "effect_context")
        effect.apply(effect_context['source'].cell, context)
        effect.cancel()
        
class AlterDamage(MetaEffect):

    info_message = "lul"
    
    def __init__(self, multiplier, **kwargs):
        super().__init__(**kwargs)
        self.multiplier = multiplier
        
    def _apply(self, effect, context, effect_context):
        print(context, "context")
        print(effect_context, "effect_context")
        with self.configure(context) as c, effect.configure(effect_context) as ec:
            effect.amount = int(ec.amount * c.multiplier)
        