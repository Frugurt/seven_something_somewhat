from .base.effect import (
    UnitEffect,
    MetaEffect,
    EFFECTS
)


class Move(UnitEffect):

    info_message = "{} move to {}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_coord = None

    def configure(self, target_coord):
        self.target_coord = target_coord

    # def _apply(self, source_action, target):

    def _apply(self, target, source_action):
        # if cell.object:
        print(self.info_message.format(target, self.target_coord))
        print(target.object)
        target.object.move(self.target_coord)
        self.info_message = self.info_message.format(target, self.target_coord)
        super()._apply(target, source_action)


class Damage(UnitEffect):

    info_message = "{} take {} damage"

    def __init__(self, amount, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount

    def _apply(self, target, source_action):
        # if cell.object:
            # for cell in cells:
            #     if cell.object:
        target.object.stats.health -= self.amount
        self.info_message = self.info_message.format(target.object, self.amount)
        super()._apply(target, source_action)


class AddStatus(UnitEffect):

    info_message = "add {} to {}"

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        self.status = status

    def _apply(self, target, source_action):
        # if cell.object:
        target.object.add_status(self.status)
        self.info_message = self.info_message.format(self.status, target.object)
        super()._apply(target, source_action)


class RemoveStatus(UnitEffect):

    info_message = "remove {} from {}"

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        self.status = status

    def _apply(self, target, source_action):
        # if cell.object:
        target.object.remove_status(self.status)
        self.info_message = self.info_message.format(self.status, target.object)
        super()._apply(target, source_action)


class Reflect(MetaEffect):

    info_message = "reflect {} to {}"

    def _apply(self, effect, source_action, effect_source_action):
        effect.apply(source_action, effect_source_action.owner.cell)


EFFECTS.update({
    'Move': Move,
    'Damage': Damage,
    'AddStatus': AddStatus,
    'RemoveStatus': RemoveStatus,
    'Reflect': Reflect,
})
