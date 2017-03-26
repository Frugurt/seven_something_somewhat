from .base.status import (
    Status,
    STATUSES,
)
from .base.trigger import TRIGGERS


class WithRifle(Status):

    name = "WithRifle"

    def on_add(self, target):
        target.stats.unit_state = "rifle"

    def on_remove(self, target):
        target.stats.unit_state = "sword"


class Parry(Status):

    name = "Parry"

    def on_add(self, target):
        target.add_trigger(TRIGGERS['Parry']())

    def on_remove(self, target):
        target.remove_trigger(TRIGGERS['Parry']())


STATUSES.update({
    "WithRifle": WithRifle,
    "Parry": Parry,
})
