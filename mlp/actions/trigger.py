from .base.trigger import (
    Trigger,
    TRIGGERS
)
from .effect import (
    Reflect,
    RemoveStatus,
    # UnitEffect,
)


class Parry(Trigger):

    name = "Parry"
    events = ["on_turn_start", "on_take_damage"]
    on_take_damage = [Reflect()]
    # on_start_turn = [RemoveStatus(Parry())]


TRIGGERS.update({
    'Parry': Parry,
})
