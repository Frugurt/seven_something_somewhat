from collections.abc import Iterable
class Effect:

    info_message = ""

    def __init__(self, **kwargs):
        # self.owner = owner
        # self.source = source
        self.info_message = self.info_message

    def configure(self, **kwargs):
        pass

    def _apply(self, source_action, cell):
        source_action.owner.action_log.append(self.info_message)

    def apply(self, source_action, cells):
        if not isinstance(cells, Iterable):
            cells = [cells]
        for cell in cells:
            self._apply(source_action, cell)
        # source_action.owner.action_log.append(self.info_message)

    def copy(self):
        return self.__class__(**vars(self))


class Move(Effect):

    info_message = "{} move to {}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_coord = None

    def configure(self, target_coord):
        self.target_coord = target_coord

    # def _apply(self, source_action, target):

    def _apply(self, source_action, cell):
        if cell.object:
            print(self.info_message.format(cell, self.target_coord))
            print(cell.object)
            cell.object.move(self.target_coord)
            self.info_message = self.info_message.format(cell, self.target_coord)
            super()._apply(source_action, cell)


class Damage(Effect):

    info_message = "{} take {} damage"

    def __init__(self, amount, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount

    def _apply(self, source_action, cell):
        if cell.object:
            # for cell in cells:
            #     if cell.object:
            cell.object.stats.health -= self.amount
            self.info_message = self.info_message.format(cell.object, self.amount)
            super()._apply(source_action, cell)


class AddStatus(Effect):

    info_message = "add {} to {}"

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        self.status = status

    def _apply(self, source_action, cell):
        if cell.object:
            cell.object.add_status(self.status)
            self.info_message = self.info_message.format(self.status, cell.object)
            super()._apply(source_action, cell)


class RemoveStatus(Effect):

    info_message = "remove {} from {}"

    def __init__(self, status, **kwargs):
        super().__init__(**kwargs)
        self.status = status

    def _apply(self, source_action, cell):
        if cell.object:
            cell.object.remove_status(self.status)
            self.info_message = self.info_message.format(self.status, cell.object)
            super()._apply(source_action, cell)


EFFECTS = {
    'Move': Move,
    'Damage': Damage,
    'AddStatus': AddStatus,
    'RemoveStatus': RemoveStatus,
}