from .effect import (
    UnitEffect,
    MetaEffect,
    EFFECTS,
)
from .status import (
    Status,
    STATUSES,
)
from .trigger import (
    Trigger,
    TRIGGERS,
)


class Move(UnitEffect):

    info_message = "{} move to {}"

    def __init__(self, **kwargs):
        self.target_coord = kwargs['target_coord']
        print("TARGET COORD", self.target_coord)
        super().__init__(**kwargs)

    # def _apply(self, source_action, target):

    def _apply(self, target, context):
        print("CONTEXT", context['action'].target_coord)
        with self.configure(context) as c:
            print("CONTEXT", vars(c))
            print(self.info_message.format(target, c.target_coord))
            print("context target coord", c.target_coord)
            target.move(c.target_coord)
            self.info_message = self.info_message.format(target, self.target_coord)
            super()._apply(target, context)


class Damage(UnitEffect):

    info_message = "{} take {} damage"

    def __init__(self, amount, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount

    def _apply(self, target, context):
        # if cell.object:
            # for cell in cells:
            #     if cell.object:
        target.stats.health -= self.amount
        self.info_message = self.info_message.format(target, self.amount)
        super()._apply(target, context)


class AddStatus(UnitEffect):

    info_message = "add {} to {}"

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        self.status = status

    def _apply(self, target, context):
        # if cell.object:
        status = self.status.copy()
        status.configure(context=context)
        target.add_status(status)
        self.info_message = self.info_message.format(self.status, target)
        super()._apply(target, context)


class RemoveStatus(UnitEffect):

    info_message = "remove {} from {}"

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        self.status = status

    def _apply(self, target, source):
        # if cell.object:
        target.remove_status(self.status)
        self.info_message = self.info_message.format(self.status, target)
        print(self.info_message)
        super()._apply(target, source)


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


class WithRifle(Status):

    name = "WithRifle"

    def on_add(self, target):
        target.stats.unit_state = "rifle"

    def on_remove(self, target):
        target.stats.unit_state = "sword"


class Parry(Status):

    name = "Parry"

    def on_add(self, target):
        target.add_trigger(ParryTrigger(context=self.context))

    def on_remove(self, target):
        target.remove_trigger(ParryTrigger())


class ParryTrigger(Trigger):

    name = "Parry"
    events = ["on_phase_start", "on_take_damage"]
    on_take_damage = [Reflect()]#, RemoveStatus(Parry())]
    on_phase_start = [RemoveStatus(Parry())]
